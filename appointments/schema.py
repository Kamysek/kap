import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from .models import Appointment
from account.models import CustomUser
from klinischesanwendungsprojekt.mailUtils import VIPreminder,VIPcancel


def isAppointmentFree(newAppointment):
    allAppointments = Appointment.objects.all()
    for existingAppointment in allAppointments:
        if ((   newAppointment.appointment_start > existingAppointment.appointment_start and newAppointment.appointment_start < existingAppointment.appointment_end) or (
                newAppointment.appointment_end > existingAppointment.appointment_start   and newAppointment.appointment_start < existingAppointment.appointment_end) or (
                newAppointment.appointment_start < existingAppointment.appointment_start and newAppointment.appointment_end > existingAppointment.appointment_end)):
            # Invalid Appointment time
            return False
    return True



def hasGroup(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


def checkAppointmentFormat(newAppointment):
    print(str(newAppointment.appointment_end - newAppointment.appointment_start))
    if (newAppointment.appointment_end - newAppointment.appointment_start).total_seconds() < 250:
        raise GraphQLError("Appointment too short ( < 5 min)")


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['title', 'appointment_start', 'appointment_end', 'taken']


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor', "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_title(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor', "Patient"], info):
            return self.title
        return None

    @login_required
    def resolve_comment_doctor(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor'], info)or self.patient == info.context.user:
            return self.comment_doctor
        return None

    @login_required
    def resolve_comment_patient(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor'], info) or self.patient == info.context.user:
            return self.comment_patient
        return None

    @login_required
    def resolve_patient(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor'], info) or self.patient == info.context.user:
            return self.patient
        return None

    @login_required
    def resolve_created_at(self, info):
        if hasGroup(["Admin", "Doctor","Labor"], info):
            return self.created_at
        return None

    @login_required
    def resolve_appointment_start(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor', "Patient"], info):
            return self.appointment_start
        return None

    @login_required
    def resolve_appointment_end(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor', "Patient"], info):
            return self.appointment_end
        return None

    @login_required
    def resolve_taken(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor', "Patient"], info):
            return self.taken
        return None


class CreateAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        title = graphene.String(required=True)
        comment_doctor = graphene.String()
        appointment_start = graphene.DateTime(required=True)
        appointment_end = graphene.DateTime(required=True)
        patient = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            if input.get('patient'):
                try:
                    patient = CustomUser.objects.get(pk=from_global_id(input.get('patient'))[1])
                    if patient.email_notification:
                        VIPreminder(patient)
                except Appointment.DoesNotExist:
                    raise GraphQLError('Patient does not exist!')
            appointment_instance = Appointment(title=input.get('title'),
                                               comment_doctor="" if input.get('comment_doctor') is None else input.get(
                                                   'comment_doctor'),
                                               patient=None if input.get('patient') is None else patient,
                                               appointment_start=input.get('appointment_start'),
                                               appointment_end=input.get('appointment_end'),
                                               taken=False)
            checkAppointmentFormat(appointment_instance)
            if not isAppointmentFree(appointment_instance):
                raise GraphQLError("Selected time slot overlaps with existing appointment")

            appointment_instance.save()
            return CreateAppointment(appointment=appointment_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a appointment!')


class UpdateAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)
        title = graphene.String()
        comment_doctor = graphene.String()
        comment_patient = graphene.String()
        appointment_start = graphene.DateTime()
        appointment_end = graphene.DateTime()
        patient = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance:
                    if hasGroup(["Admin", "Doctor"], info):
                        if input.get('title'):
                            appointment_instance.title = input.get('title')
                        if input.get('comment_doctor'):
                            appointment_instance.comment_doctor = input.get('comment_doctor')
                        if input.get('appointment_start'):
                            appointment_instance.appointment_start = input.get('appointment_start')
                        if input.get('appointment_end'):
                            appointment_instance.appointment_end = input.get('appointment_end')
                        if input.get('patient'):
                            appointment_instance.patient = input.get('patient')
                            appointment_instance.taken = True
                            if patient.email_notification:
                                VIPreminder(patient)
                        #appointment_instance.delete()
                        #if not isAppointmentFree(appointment_instance,Appointment.objects.all().exclude(calendar__appointment__id=1)):
                        #    raise GraphQLError("Selected time slot overlaps with existing appointment")
                        appointment_instance.save()
                        return CreateAppointment(appointment=appointment_instance)
                    elif hasGroup(["Patient"], info) and (appointment_instance.taken == False or appointment_instance.patient == info.context.user):
                        appointment_instance.patient = info.context.user
                        appointment_instance.comment_patient = "" if input.get(
                            'comment_patient') is None else input.get('comment_patient'),
                        appointment_instance.taken = True
                        appointment_instance.save()
                        if info.context.user.email_notification:
                            VIPreminder(info.context.user)
                    return CreateAppointment(appointment=appointment_instance)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a appointment!')


class DeleteAppointment(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)
        remove_patient = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance:
                    if hasGroup(["Admin", "Doctor"], info):
                        if input.get('remove_patient'):
                            appointment_instance.patient = None
                            appointment_instance.comment_patient = ""
                            appointment_instance.taken = False
                            appointment_instance.save()
                        else:
                            appointment_instance.delete()
                    elif hasGroup(["Patient"], info):
                        if appointment_instance.patient == info.context.user:
                            appointment_instance.patient = None
                            appointment_instance.comment_patient = ""
                            appointment_instance.taken = False
                            appointment_instance.save()
                            if info.context.user.email_notification:
                                VIPcancel(info.context.user)
                    return DeleteAppointment(ok=True)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a appointment!')


class Query(graphene.ObjectType):
    get_appointment = graphene.relay.Node.Field(AppointmentType)
    get_appointments = DjangoFilterConnectionField(AppointmentType, filterset_class=AppointmentFilter)


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
    update_appointment = UpdateAppointment.Field()
    delete_appointment = DeleteAppointment.Field()
