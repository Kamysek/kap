import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from .models import Appointment, Calendar


def isAppointmentFree(newAppointment, allAppointments):
    for existingAppointment in allAppointments:
        if newAppointment.calendar_id == existingAppointment.calendar_id and ((
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


class CalendarFilter(django_filters.FilterSet):
    class Meta:
        model = Calendar
        fields = ['name', 'doctor']


class CalendarType(DjangoObjectType):
    class Meta:
        model = Calendar
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_name(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.name
        return None

    @login_required
    def resolve_doctor(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.doctor
        return None


class CreateCalendar(graphene.relay.ClientIDMutation):
    calendar = graphene.Field(CalendarType)

    class Input:
        name = graphene.String(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            if info.context.user is None:
                raise GraphQLError('Please provide user!')
            calendar_instance = Calendar(name=input.get('name'), doctor=info.context.user)
            calendar_instance.save()
            return CreateCalendar(calendar=calendar_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a calendar!')


class UpdateCalendar(graphene.relay.ClientIDMutation):
    calendar = graphene.Field(CalendarType)

    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                calendar_instance = Calendar.objects.get(pk=from_global_id(input.get('id'))[1])
                if calendar_instance:
                    if input.get('name'):
                        calendar_instance.name = input.get('name')
                    calendar_instance.save()
                    return CreateCalendar(calendar=calendar_instance)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a calendar!')


class DeleteCalendar(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    calendar = graphene.Field(CalendarType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                calendar_instance = Calendar.objects.get(pk=from_global_id(input.get('id'))[1])
                if calendar_instance:
                    calendar_instance.delete()
                    return DeleteCalendar(ok=True)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a calendar!')


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['title', 'calendar', 'appointment_start', 'appointment_end', 'taken']


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_title(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.title
        return None

    @login_required
    def resolve_comment_doctor(self, info):
        if hasGroup(["Admin", "Doctor"], info):
            return self.comment_doctor
        return None

    @login_required
    def resolve_comment_patient(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.patient == info.context.user:
            return self.comment_patient
        return None

    @login_required
    def resolve_calendar(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.calendar
        return None

    @login_required
    def resolve_patient(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.patient == info.context.user:
            return self.patient
        return None

    @login_required
    def resolve_created_at(self, info):
        if hasGroup(["Admin", "Doctor"], info):
            return self.created_at
        return None

    @login_required
    def resolve_appointment_start(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            if not self.taken:
                return self.appointment_start
            else:
                if hasGroup(["Admin", "Doctor"], info) or self.patient == info.context.user:
                    return self.appointment_start
        return None

    @login_required
    def resolve_appointment_end(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            if not self.taken:
                return self.appointment_end
            else:
                if hasGroup(["Admin", "Doctor"], info) or self.patient == info.context.user:
                    return self.appointment_end
        return None

    @login_required
    def resolve_taken(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.taken
        return None


class CreateAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        title = graphene.String(required=True)
        comment_doctor = graphene.String()
        calendar = graphene.ID(required=True)
        appointment_start = graphene.DateTime(required=True)
        appointment_end = graphene.DateTime(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                get_calendar = Calendar.objects.get(pk=from_global_id(input.get('calendar'))[1])
                if get_calendar:
                    appointment_instance = Appointment(title=input.get('title'),
                                                       comment_doctor="" if input.get('comment_doctor') is None else input.get('comment_doctor'),
                                                       calendar=get_calendar,
                                                       appointment_start=input.get('appointment_start'),
                                                       appointment_end=input.get('appointment_end'),
                                                       taken=False)
                    checkAppointmentFormat(appointment_instance)
                    appointment_instance.save()
                    return CreateAppointment(appointment=appointment_instance)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a appointment!')


class UpdateAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)
        title = graphene.String()
        comment_doctor = graphene.String()
        calendar = graphene.ID()
        appointment_start = graphene.DateTime()
        appointment_end = graphene.DateTime()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance:
                    if input.get('title'):
                        appointment_instance.title = input.get('title')
                    if input.get('comment_doctor'):
                        appointment_instance.comment_doctor = input.get('comment_doctor')
                    if input.get('calendar'):
                        try:
                            get_calendar = Calendar.objects.get(pk=from_global_id(input.get('calendar'))[1])
                            if get_calendar:
                                appointment_instance.calendar = get_calendar
                        except Calendar.DoesNotExist:
                            raise GraphQLError('Calendar does not exist!')
                    if input.get('appointment_start'):
                        appointment_instance.appointment_start = input.get('appointment_start')
                    if input.get('appointment_end'):
                        appointment_instance.appointment_end = input.get('appointment_end')

                    # if not isAppointmentFree(appointment_instance,
                    #                         Appointment.objects.all().exclude(calendar__appointment__id=1)):
                    #    raise GraphQLError("Invalid Time selected")

                    appointment_instance.save()
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

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance:
                    appointment_instance.delete()
                    return DeleteAppointment(ok=True)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a appointment!')


class TakeAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)
        comment_patient = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Patient", "Admin"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance and not appointment_instance.taken:
                    appointment_instance.patient = info.context.user
                    appointment_instance.comment_patient = "" if input.get('comment_patient') is None else input.get('comment_patient'),
                    appointment_instance.taken = True
                    appointment_instance.save()
                    return TakeAppointment(appointment=appointment_instance)
                else:
                    raise GraphQLError('Appointment is already taken!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to take a appointment!')


class UpdateTakenAppointment(graphene.relay.ClientIDMutation):
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)
        comment_patient = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Patient", "Admin"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance.patient == info.context.user:
                    if input.get('comment_patient'):
                        appointment_instance.comment_patient = input.get('comment_patient')
                        appointment_instance.save()
                        return UpdateTakenAppointment(appointment=appointment_instance)
                else:
                    raise UnauthorisedAccessError(message='No permissions to change a taken appointment!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a taken appointment!')


class DeleteTakenAppointment(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    appointment = graphene.Field(AppointmentType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Patient", "Admin"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=from_global_id(input.get('id'))[1])
                if appointment_instance.patient == info.context.user:
                    appointment_instance.patient = None
                    appointment_instance.comment_patient = ""
                    appointment_instance.taken = False
                    appointment_instance.save()
                    return DeleteTakenAppointment(ok=True)
                else:
                    raise UnauthorisedAccessError(message='No permissions to delete a taken appointment!')
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a taken appointment!')


class Query(graphene.ObjectType):

    get_calendar = graphene.relay.Node.Field(CalendarType)
    get_calendars = DjangoFilterConnectionField(CalendarType, filterset_class=CalendarFilter)

    get_appointment = graphene.relay.Node.Field(AppointmentType)
    get_appointments = DjangoFilterConnectionField(AppointmentType, filterset_class=AppointmentFilter)


class Mutation(graphene.ObjectType):
    create_calendar = CreateCalendar.Field()
    create_appointment = CreateAppointment.Field()
    take_appointment = TakeAppointment.Field()

    update_calendar = UpdateCalendar.Field()
    update_appointment = UpdateAppointment.Field()
    update_taken_appointment = UpdateTakenAppointment.Field()

    delete_calendar = DeleteCalendar.Field()
    delete_appointment = DeleteAppointment.Field()
    delete_taken_appointment = DeleteTakenAppointment.Field()
