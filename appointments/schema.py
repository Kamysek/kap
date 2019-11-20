import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from datetime import datetime
from graphql_jwt.decorators import login_required
from .models import Appointment, Calendar


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class CalendarType(DjangoObjectType):
    class Meta:
        model = Calendar


class CalendarInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)


class CreateCalendar(graphene.Mutation):
    class Arguments:
        input = CalendarInput(required=True)

    calendar = graphene.Field(CalendarType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('appointments.can_add_calendar'):
            if input.name is not None and info.context.user is not None:
                calendar_instance = Calendar(name=input.name, doctor=info.context.user)
                calendar_instance.save()
                return CreateCalendar(calendar=calendar_instance)
            else:
                raise Exception('Please provide complete information!')
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
                    if input.name:
                        calendar_instance.name = input.name
                    calendar_instance.save()
                    return CreateCalendar(board=calendar_instance)
            except Calendar.DoesNotExist:
                raise Exception('Calendar does not exist!')
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
                raise Exception('Calendar does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a calendar!')


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment


class AppointmentInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    comment_doctor = graphene.String(required=True)
    calendar = graphene.Int(required=True)
    appointment_start = graphene.DateTime()
    appointment_end = graphene.DateTime()


class CreateAppointment(graphene.Mutation):
    class Arguments:
        input = AppointmentInput(required=True)

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('appointments.can_add_appointment'):
            if input.title is not None and input.comment_doctor is not None and input.calendar is not None and input.appointment_start is not None and input.appointment_end is not None and info.context.user is not None:
                try:
                    get_calendar = Calendar.objects.get(pk=input.calendar)
                    if get_calendar:
                        appointment_instance = Appointment(title=input.title, comment_doctor=input.comment,
                                                           calendar=get_calendar, patient=None,
                                                           created_At=datetime.now(),
                                                           appointment_start=input.appointment_start,
                                                           appointment_end=input.appointment_end, taken=False)
                        appointment_instance.save()
                        return CreateAppointment(appointment=appointment_instance)
                except Calendar.DoesNotExist:
                    raise Exception('Calendar does not exist!')
            else:
                raise Exception('Please provide complete information!')
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
                                appointment_instance.calendar = get_calendar
                        except Calendar.DoesNotExist:
                            raise Exception('Calendar does not exist!')
                    if input.appointment_start:
                        appointment_instance.appointment_start = input.appointment_start
                    if input.appointment_end:
                        appointment_instance.appointment_end = input.appointment_end
                    appointment_instance.save()
                    return CreateAppointment(appointment=appointment_instance)
            except Appointment.DoesNotExist:
                raise Exception('Appointment does not exist!')
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
                raise Exception('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a appointment!')


class CreateAppointmentPatient(graphene.Mutation):
    class Arguments:
        appointment_id = graphene.Int(required=True)
        comment_patient = graphene.String()

    appointment = graphene.Field(AppointmentType)

    @login_required
    def mutate(self, info, appointment_id, comment_patient):
        if info.context.user.has_perm('appointments.can_add_appointment_patient'):
            try:
                appointment_instance = Appointment.objects.get(pk=appointment_id)
                if appointment_instance and not appointment_instance.taken:
                    appointment_instance.patient = info.context.user
                    appointment_instance.comment_patient = comment_patient
                    appointment_instance.taken = True
                    appointment_instance.save()
                    return CreateAppointmentPatient(appointment=appointment_instance)
                else:
                    raise Exception('Appointment is already taken!')
            except Calendar.DoesNotExist:
                raise Exception('Appointment does not exist!')
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
                raise Exception('Appointment does not exist!')
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
                if appointment_instance.patient == info.context.user:
                    appointment_instance.patient = None
                    appointment_instance.taken = False
                    return DeleteAppointmentPatient(ok=True)
                else:
                    raise UnauthorisedAccessError(message='No permissions to change this patient appointment!')
            except Appointment.DoesNotExist:
                raise Exception('Appointment does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a patient appointment!')


class Query(graphene.ObjectType):
    my_calendars = graphene.List(CalendarType)
    all_calendars = graphene.List(CalendarType)
    all_appointments_doctor = graphene.List(AppointmentType)
    one_calendar_appointments_doctor = graphene.List(AppointmentType, ident=graphene.Int())
    appointments_patient = graphene.List(AppointmentType)

    @login_required
    def my_calendars(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_calendar'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                return Calendar.objects.fiter(doctor=info.context.user)
            else:
                raise UnauthorisedAccessError(message='No permissions to see the calendars!')
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
                my_calendars = self.my_calendars()
                all_appointments = []
                for m_c in my_calendars:
                    all_appointments.append(Appointment.objects.fiter(calendar=m_c))
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
                        return Appointment.objects.get(calendar=ident)
                    except Calendar.DoesNotExist:
                        raise Exception('Calendar does not exist!')
            else:
                raise UnauthorisedAccessError(message='No permissions to see the appointments!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the appointments!')

    @login_required
    def resolve_appointments_patient(self, info, **kwargs):
        if info.context.user.has_perm('appointments.can_view_appointment_patient'):
            try:
                return Appointment.objects.get(patient=info.context.user)
            except Calendar.DoesNotExist:
                raise Exception('No appointments exist!')
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
