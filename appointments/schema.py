import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
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


class CalendarInput(graphene.InputObjectType):
    name = graphene.String()


class CreateCalendar(graphene.Mutation):
    class Arguments:
        input = CalendarInput(required=True)

    calendar = graphene.Field(CalendarType)

    @login_required
    def mutate(self, info, input=None):
        if hasGroup(["Admin", "Doctor"], info):
            if input.name is None:
                raise GraphQLError('Please provide name!')
            if info.context.user is None:
                raise GraphQLError('Please provide user!')
            calendar_instance = Calendar(name=input.name, doctor=info.context.user)
            calendar_instance.save()
            return CreateCalendar(calendar=calendar_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a calendar!')


class UpdateCalendar(graphene.Mutation):
    class Arguments:
        calendar_id = graphene.Int(required=True)
        input = CalendarInput(required=True)

    calendar = graphene.Field(CalendarType)

    @login_required
    def mutate(self, info, calendar_id, input=None):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                calendar_instance = Calendar.objects.get(pk=calendar_id)
                if calendar_instance:
                    if input.name:
                        calendar_instance.name = input.name
                    calendar_instance.save()
                    return CreateCalendar(calendar=calendar_instance)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a calendar!')


class DeleteCalendar(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        calendar_id = graphene.Int(required=True)

    calendar = graphene.Field(CalendarType)

    @login_required
    def mutate(self, info, calendar_id):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                calendar_instance = Calendar.objects.get(pk=calendar_id)
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


class AppointmentInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    comment_doctor = graphene.String()
    calendar = graphene.Int()
    appointment_start = graphene.DateTime()
    appointment_end = graphene.DateTime()


class CreateAppointment(graphene.Mutation):
    class Arguments:
        input = AppointmentInput(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, input=None):
        if hasGroup(["Admin", "Doctor"], info):
            if input.title is None:
                raise GraphQLError('Please provide title!')
            if input.calendar is None:
                raise GraphQLError('Please provide calendar!')
            if input.appointment_start is None:
                raise GraphQLError('Please provide appointment start!')
            if input.appointment_end is None:
                raise GraphQLError('Please provide appointment end!')
            if info.context.user is None:
                raise GraphQLError('Please provide user!')
            try:
                get_calendar = Calendar.objects.get(pk=input.calendar)
                if get_calendar:
                    appointment_instance = Appointment(title=input.title,
                                                       comment_doctor="" if input.comment_doctor is None else input.comment_doctor,
                                                       calendar=get_calendar,
                                                       appointment_start=input.appointment_start,
                                                       appointment_end=input.appointment_end,
                                                       taken=False)
                    checkAppointmentFormat(appointment_instance)
                    appointment_instance.save()
                    return CreateAppointment(appointment=appointment_instance)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a appointment!')


class UpdateAppointment(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        input = AppointmentInput(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, input=None):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance:
                    if input.title:
                        appointment_instance.title = input.title
                    if input.comment_doctor:
                        appointment_instance.comment_doctor = input.comment_doctor
                    if input.calendar:
                        try:
                            get_calendar = Calendar.objects.get(pk=input.calendar)
                            if get_calendar:
                                appointment_instance.calendar = get_calendar
                        except Calendar.DoesNotExist:
                            raise GraphQLError('Calendar does not exist!')
                    if input.appointment_start:
                        appointment_instance.appointment_start = input.appointment_start
                    if input.appointment_end:
                        appointment_instance.appointment_end = input.appointment_end

                    # if not isAppointmentFree(appointment_instance,
                    #                         Appointment.objects.all().exclude(calendar__appointment__id=1)):
                    #    raise GraphQLError("Invalid Time selected")

                    appointment_instance.save()
                    return CreateAppointment(appointment=appointment_instance)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a appointment!')


class DeleteAppointment(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        appointment_id = graphene.Int(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance:
                    appointment_instance.delete()
                    return DeleteAppointment(ok=True)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a appointment!')


class TakeAppointment(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        comment_patient = graphene.String()

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, comment_patient):
        if hasGroup(["Patient"], info) and self.patient == info.context.user:
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance and not appointment_instance.taken:
                    appointment_instance.patient = info.context.user
                    appointment_instance.comment_patient = comment_patient
                    appointment_instance.taken = True
                    appointment_instance.save()
                    return TakeAppointment(appointment=appointment_instance)
                else:
                    raise GraphQLError('Appointment is already taken!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to take a appointment!')


class UpdateTakenAppointment(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        comment_patient = graphene.String()

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, comment_patient):
        if hasGroup(["Patient"], info) and self.patient == info.context.user :
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance.patient == info.context.user:
                    if comment_patient:
                        appointment_instance.comment_patient = comment_patient
                        appointment_instance.save()
                        return UpdateTakenAppointment(appointment=appointment_instance)
                else:
                    raise UnauthorisedAccessError(message='No permissions to change a taken appointment!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a taken appointment!')


class DeleteTakenAppointment(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        appointment_id = graphene.Int(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id):
        if hasGroup(["Patient"], info) and self.patient == info.context.user:
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
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


    """
    get_calendar = graphene.List(CalendarType, id=graphene.Int(required=False, default_value=None))
    appointment = graphene.List(AppointmentType, id=graphene.Int(required=False, default_value=None),
                                title=graphene.String(required=False, default_value=None),
                                taken=graphene.Boolean(required=False, default_value=None),
                                only_mine=graphene.Boolean(required=False, default_value=None))

    @login_required
    def resolve_calendar(self, info, **kwargs):
        id = kwargs.get('id')
        objects = Calendar.objects.all()

        if id is not None:
            print("FILTERING")
            objects = objects.filter(id=id)
        return objects

    @login_required
    def resolve_appointment(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        taken = kwargs.get('taken')
        only_mine = kwargs.get('only_mine')
        objects = Appointment.objects.all()
        if id is not None:
            objects = objects.filter(id=id)
        if title is not None:
            objects = objects.filter(title=title)
        if taken is not None:
            objects = objects.filter(taken=taken)
        if only_mine:
            objects = objects.filter(patient_id=info.context.user.id)
        return objects

    """


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
