from datetime import timedelta
import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from .models import Appointment
from account.models import CustomUser
from klinischesanwendungsprojekt.mailUtils import VIPreminder, VIPcancel
import datetime
from django.utils.timezone import make_aware


def isAppointmentFree(newAppointment):
    allAppointments = Appointment.objects.all()
    for existingAppointment in allAppointments:
        if newAppointment == existingAppointment:
            continue
        if ((
                newAppointment.appointment_start > existingAppointment.appointment_start and newAppointment.appointment_start < existingAppointment.appointment_end) or (
                newAppointment.appointment_end > existingAppointment.appointment_start and newAppointment.appointment_start < existingAppointment.appointment_end) or (
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
        if hasGroup(["Admin", "Doctor", 'Labor'], info) or self.patient == info.context.user:
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
        if hasGroup(["Admin", "Doctor", "Labor"], info):
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

    @login_required
    def resolve_noshow(self, info):
        if hasGroup(["Admin", "Doctor", 'Labor'], info):
            return self.noshow
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


class AppointmentInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    comment_doctor = graphene.String()
    appointment_start = graphene.DateTime(required=True)
    appointment_end = graphene.DateTime(required=True)
    patient = graphene.ID()


class CreateAppointments(graphene.relay.ClientIDMutation):
    class Input:
        appointments = graphene.List(AppointmentInput)

    appointments = graphene.List(AppointmentType)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            failed_appointments = []
            for app in input.get('appointments'):
                if app.get('patient'):
                    try:
                        patient = CustomUser.objects.get(pk=from_global_id(app.get('patient'))[1])
                        if patient.email_notification:
                            VIPreminder(patient)
                    except Appointment.DoesNotExist:
                        raise GraphQLError('Patient does not exist!')
                appointment_instance = Appointment(title=app.get('title'),
                                                   comment_doctor="" if app.get('comment_doctor') is None else app.get(
                                                       'comment_doctor'),
                                                   patient=None if app.get('patient') is None else patient,
                                                   appointment_start=app.get('appointment_start'),
                                                   appointment_end=app.get('appointment_end'),
                                                   taken=False)
                checkAppointmentFormat(appointment_instance)
                if not isAppointmentFree(appointment_instance):
                    failed_appointments.append(appointment_instance)
                    continue

                appointment_instance.save()

            return CreateAppointments(appointments=failed_appointments)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a appointment!')


class BookSlots(graphene.relay.ClientIDMutation):
    class Input:
        appointmentList = graphene.List(graphene.ID)

    appointmentList = graphene.List(graphene.ID)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor", "Patient"], info):

            for app in input.get('appointmentList'):
                appointment_instance = Appointment.objects.get(pk=from_global_id(app)[1])

                if appointment_instance.taken:
                    raise GraphQLError('Appointment already taken')

            max_date = make_aware(datetime.datetime.strptime("2000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S'))
            min_date = make_aware(datetime.datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S'))

            for app in input.get('appointmentList'):
                appointment_instance = Appointment.objects.get(pk=from_global_id(app)[1])
                app_start = make_aware(datetime.datetime.strptime(
                    appointment_instance.appointment_start.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
                app_end = make_aware(datetime.datetime.strptime(appointment_instance.appointment_end.strftime('%Y-%m-%d %H:%M:%S'),
                                                     '%Y-%m-%d %H:%M:%S'))

                if app_start < min_date:
                    min_date = app_start
                if app_end > max_date:
                    max_date = app_end

            tmp_app = Appointment.objects.get(pk=from_global_id(input.get('appointmentList')[0])[1])
            appointment = Appointment(title=tmp_app.title,
                                      comment_doctor=tmp_app.comment_doctor,
                                      patient=tmp_app.patient,
                                      appointment_start=min_date,
                                      appointment_end=max_date,
                                      taken=True)
            checkAppointmentFormat(appointment)
            appointment.save()

            for app in input.get('appointmentList'):
                appointment_instance = Appointment.objects.get(pk=from_global_id(app)[1])
                appointment_instance.delete()

            return CreateAppointments(appointments=appointment)
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
        taken = graphene.Boolean()

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
                        if input.get('patient'):  # Todo: doesn't work
                            appointment_instance.patient = input.get('patient')
                            appointment_instance.taken = True
                            if appointment_instance.patient.email_notification:
                                VIPreminder(appointment_instance.patient)
                        if input.get('taken'):
                            appointment_instance.taken = input.get('taken')
                            if not input.get('taken'):
                                appointment_instance.patient = None
                            if appointment_instance.patient.email_notification:
                                VIPreminder(appointment_instance.patient)
                        checkAppointmentFormat(appointment_instance)
                        if not isAppointmentFree(appointment_instance):
                            raise GraphQLError("Selected time slot overlaps with existing appointment")
                        appointment_instance.save()
                        return CreateAppointment(appointment=appointment_instance)
                    elif hasGroup(["Patient"], info) and (
                            appointment_instance.taken == False or appointment_instance.patient == info.context.user):
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
    get_slot_lists = graphene.List(graphene.List(AppointmentType), date=graphene.DateTime(required=True),
                                   minusdays=graphene.Int(default_value=7), plusdays=graphene.Int(default_value=7))

    def resolve_get_slot_lists(self, info, **kwargs):
        qs = Appointment.objects.all().filter(taken=False)

        date = kwargs.get('date')
        minusdays = kwargs.get('minusdays')
        plusdays = kwargs.get('plusdays')



        if date:
            startdate = date - timedelta(days=minusdays)
            enddate = date + timedelta(days=plusdays)
            qs = qs.filter(appointment_start__range=[startdate, enddate])

        if info.context.user.timeslots_needed > 1:
            slot_list = []

            if minusdays is None:
                minusdays = 0
            if plusdays is None:
                plusdays = 0

            if minusdays is 0:
                start_date = date.strftime("%Y-%m-%d")
            else:
                start_date = (date - timedelta(days=minusdays)).strftime("%Y-%m-%d")

            for i in range(0, plusdays + minusdays + 1):

                start_datetime = make_aware(
                    datetime.datetime.strptime(start_date + " 00:00:00", '%Y-%m-%d %H:%M:%S') + timedelta(days=i))
                end_datetime = make_aware(
                    datetime.datetime.strptime(start_date + " 23:59:59", '%Y-%m-%d %H:%M:%S') + timedelta(days=i))

                qs_tmp = qs.filter(appointment_start__range=[start_datetime, end_datetime])

                if qs_tmp and info.context.user.timeslots_needed is 2:
                    for a in qs_tmp:
                        for b in qs_tmp:
                            if a.appointment_end == b.appointment_start:
                                slot_list.append([a, b])

                if qs_tmp and info.context.user.timeslots_needed is 3:
                    for a in qs_tmp:
                        for b in qs_tmp:
                            for c in qs_tmp:
                                if a.appointment_end == b.appointment_start and b.appointment_end == c.appointment_start:
                                    slot_list.append([a, b, c])

                if qs_tmp and info.context.user.timeslots_needed is 4:
                    for a in qs_tmp:
                        for b in qs_tmp:
                            for c in qs_tmp:
                                for d in qs_tmp:
                                    if a.appointment_end == b.appointment_start and b.appointment_end == c.appointment_start and c.appointment_end == d.appointment_start:
                                        slot_list.append([a, b, c, d])

            qs = slot_list
        return qs


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
    create_appointments = CreateAppointments.Field()
    update_appointment = UpdateAppointment.Field()
    delete_appointment = DeleteAppointment.Field()
    book_slots = BookSlots.Field()
