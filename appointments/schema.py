import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import Appointment, Calendar
from django.contrib.auth import get_user_model

"""
    title = models.CharField(max_length=50, null=True)
    comment_doctor = models.TextField(max_length=200, null=False, blank=True)
    comment_patient = models.TextField(max_length=200, null=False, blank=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    appointment_start = models.DateTimeField()
    appointment_end = models.DateTimeField()
    taken = models.BooleanField(default=False)
def remove_sensitive_appointment(user, appointment):
    if user != appointment.patient:
        appointment.patient = None
        appointment.title = None
        appointment.comment_doctor = None
        appointment.comment_patient = None
        appointment.files = None
        appointment.created_at = None
        appointment.id = 0

def remove_sensitive_data(user, queryset):
    for appointment in queryset:
        remove_sensitive_appointment(user, appointment)
"""


def isAppointmentFree(newAppointment, allAppointments):
    for existingAppointment in allAppointments:
        if newAppointment.calendar_id == existingAppointment.calendar_id and ((
                newAppointment.appointment_start > existingAppointment.appointment_start and newAppointment.appointment_start < existingAppointment.appointment_end) or (
                newAppointment.appointment_end > existingAppointment.appointment_start and newAppointment.appointment_start < existingAppointment.appointment_end) or (
                newAppointment.appointment_start < existingAppointment.appointment_start and newAppointment.appointment_end > existingAppointment.appointment_end)):
            # Invalid Appointment time
            return False
    return True


def checkAppointmentFormat(newAppointment):
    print(str(newAppointment.appointment_end - newAppointment.appointment_start))
    if (newAppointment.appointment_end - newAppointment.appointment_start).total_seconds() < 250:
        raise GraphQLError("Appointment too short ( < 5 min)")


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class CalendarType(DjangoObjectType):
    class Meta:
        model = Calendar


class CalendarInput(graphene.InputObjectType):
    name = graphene.String()


class CreateCalendar(graphene.Mutation):
    class Arguments:
        input = CalendarInput(required=True)

    calendar = graphene.Field(CalendarType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('appointments.can_add_calendar'):
            calendar_instance = Calendar(name=input.name, doctor_id=info.context.user.id)
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
        if info.context.user.has_perm('appointments.can_change_calendar'):
            try:
                calendar_instance = Calendar.objects.get(pk=calendar_id)
                if calendar_instance:
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
        if info.context.user.has_perm('appointments.can_delete_calendar'):
            try:
                calendar_instance = Calendar.objects.get(pk=calendar_id)
                if calendar_instance:
                    calendar_instance.delete()
                    return DeleteCalendar(ok=True)
            except Calendar.DoesNotExist:
                raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a calendar!')


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment


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
        if info.context.user.has_perm('appointments.can_add_appointment'):
            if input.title is not None and input.calendar is not None and input.appointment_start is not None and input.appointment_end is not None and info.context.user is not None:
                try:
                    get_calendar = Calendar.objects.get(pk=input.calendar)
                    if get_calendar:
                        appointment_instance = Appointment(title=input.title,
                                                           comment_doctor="" if input.comment_doctor is None else input.comment_doctor,
                                                           calendar_id=get_calendar.id,
                                                           appointment_start=input.appointment_start,
                                                           appointment_end=input.appointment_end, taken=False)
                        checkAppointmentFormat(appointment_instance)
                        appointment_instance.save()
                        return CreateAppointment(appointment=appointment_instance)
                except Calendar.DoesNotExist:
                    raise GraphQLError('Calendar does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a appointment!')


class UpdateAppointment(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        input = AppointmentInput(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, input=None):
        if info.context.user.has_perm('appointments.can_change_appointment'):
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
                                appointment_instance.calendar_id = get_calendar
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
        if info.context.user.has_perm('appointments.can_delete_appointment'):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance:
                    appointment_instance.delete()
                    return DeleteAppointment(ok=True)
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a appointment!')


class CreateAppointmentPatient(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        comment_patient = graphene.String(default_value="")

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, comment_patient):
        if info.context.user.has_perm('appointments.can_add_appointment_patient'):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance and not appointment_instance.taken:
                    appointment_instance.patient = info.context.user.id
                    appointment_instance.comment_patient = comment_patient
                    appointment_instance.taken = True
                    appointment_instance.save()
                    return CreateAppointmentPatient(appointment=appointment_instance)
                else:
                    raise GraphQLError('Appointment is already taken!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a patient appointment!')


class UpdateAppointmentPatient(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        comment_patient = graphene.String()

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, comment_patient):
        if info.context.user.has_perm('appointments.can_change_appointment_patient'):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance.patient == info.context.user:
                    if comment_patient:
                        appointment_instance.comment_patient = comment_patient
                        appointment_instance.save()
                        return CreateAppointmentPatient(appointment=appointment_instance)
                else:
                    raise UnauthorisedAccessError(message='No permissions to change this patient appointment!')
            except Calendar.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a patient appointment!')


class DeleteAppointmentPatient(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        appointment_id = graphene.Int(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id):
        if info.context.user.has_perm('appointments.can_delete_appointment_patient'):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance.patient == info.context.user.id:
                    appointment_instance.patient = None
                    appointment_instance.taken = False
                    appointment_instance.save()
                    return DeleteAppointmentPatient(ok=True)
                else:
                    raise UnauthorisedAccessError(message='No permissions to change this patient appointment!')
            except Appointment.DoesNotExist:
                raise GraphQLError('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a patient appointment!')


class Query(graphene.ObjectType):
    get_calendar = graphene.List(CalendarType, id=graphene.Int())
    my_calendars = graphene.List(CalendarType)
    all_calendars = graphene.List(CalendarType)
    all_appointments_doctor = graphene.List(AppointmentType)
    one_calendar_appointments_doctor = graphene.List(AppointmentType, ident=graphene.Int())
    appointments_patient = graphene.List(AppointmentType)

    @login_required
    def resolve_get_calendar(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_calendar'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    elem = Calendar.objects.filter(pk=id)
                    return elem.get(0)
                except Calendar.DoesNotExist:
                    raise GraphQLError('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the calendars!')

    @login_required
    def resolve_my_calendars(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_calendar'):
            # f = Calendar.objects.filter(filter_fields=["doctor"])
            return Calendar.objects.filter(doctor=info.context.user)
        else:
            raise UnauthorisedAccessError(message='No permissions to see the calendars!')

    @login_required
    def resolve_all_calendars(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_calendar'):
            return Calendar.objects.all()
        else:
            raise UnauthorisedAccessError(message='No permissions to see the calendars!')

    @login_required
    def resolve_all_appointments_doctor(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_appointment'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                my_calendars = Calendar.objects.filter(doctor=info.context.user)
                all_appointments = []
                for m_c in my_calendars:
                    all_appointments.extend(Appointment.objects.filter(calendar=m_c))
                return all_appointments
            else:
                raise UnauthorisedAccessError(message='No permissions to see the appointments!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the appointments!')

    @login_required
    def resolve_one_calendar_appointments_doctor(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_appointment'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                ident = kwargs.get('ident')
                if ident is not None:
                    try:
                        return Appointment.objects.filter(calendar=ident)
                    except Calendar.DoesNotExist:
                        raise GraphQLError('Calendar does not exist!')
            else:
                raise UnauthorisedAccessError(message='No permissions to see the appointments!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the appointments!')

    @login_required
    def resolve_appointments_patient(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_appointment_patient'):
            try:
                return Appointment.objects.filter(patient=info.context.user)
            except Appointment.DoesNotExist:
                raise GraphQLError('No appointments exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the appointments!')


class Mutation(graphene.ObjectType):
    create_calendar = CreateCalendar.Field()
    create_appointment = CreateAppointment.Field()
    create_appointment_patient = CreateAppointmentPatient.Field()

    update_calendar = UpdateCalendar.Field()
    update_appointment = UpdateAppointment.Field()
    update_appointment_patient = UpdateAppointmentPatient.Field()

    delete_calendar = DeleteCalendar.Field()
    delete_appointment = DeleteAppointment.Field()
    delete_appointment_patient = DeleteAppointmentPatient.Field()
