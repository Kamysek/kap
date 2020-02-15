from datetime import timedelta

from django.utils import timezone
from graphql import GraphQLError
from graphql_relay import from_global_id

from appointments.models import Appointment
from django.contrib.auth import get_user_model
from utils.mailUtils import sendOverdueMail, sendDayReminderMail, sendWeekReminderMail

User = get_user_model()


def valid_id(global_id, type):
    """Checks that the given graphql id is relevant to specific type and that the queried object exists"""
    try:
        if str(type) == str(from_global_id(global_id)[0]):
            return from_global_id(global_id)
    except:
        raise GraphQLError("Invalid ID")
    raise GraphQLError("InvalidID")


def has_group(groups, info):
    """
    TODO: We used group authentication because fullblown CRUD authentication would have introduced unnecessary complexity
    HOWEVER: this function call always does a db request leading to decreased performance, while django permissions are cached automatically. a rewrite would probably boost performance
    """
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


def countSeperateAppointments(appointments):
    if appointments.count() <= 1:
        return appointments.count()
    tmp = appointments[0]
    count = 1
    for app in appointments:
        if app.appointment_start.date() != tmp.appointment_start.date():
            count += 1
        tmp = app
    return count


def checkUserOverdue(user):
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("daysUntil")
    appointmentsAttended = Appointment.objects.all().filter(patient=user).filter(noshow=False).order_by('appointment_start')  # get number of  attended appointments
    appointmentCount = countSeperateAppointments(appointmentsAttended)
    if appointmentCount == checkups.count() or Appointment.objects.all().filter(patient=user).filter(
            appointment_start__gte=timezone.now()).count() > 0:  # Finished study or already has upcoming appointment
        user.checkup_overdue = None
        user.overdue_notified = timezone.now() - timedelta(days=10)
        user.save()
        return
    nextCheckup = checkups[appointmentCount]
    user.next_checkup = user.date_joined + timedelta(days=nextCheckup.daysUntil)
    if (nextCheckup.daysUntil < days_since_joined):
        user.checkup_overdue = user.date_joined + timedelta(days=nextCheckup.daysUntil)  # Duplicate but too far in now to change it
        if (days_since_joined - nextCheckup.daysUntil) > 3 and (
                (timezone.now() - user.overdue_notified) > timedelta(days=7)):  # Notify if patient is more than 3 days overdue or last Notification is 1 week overdue
            if sendOverdueMail(user, nextCheckup.name) != -1:
                user.overdue_notified = timezone.now()
    else:
        user.checkup_overdue = None
        user.overdue_notified = timezone.now() - timedelta(days=10)
    user.save()


def updateUserOverdue(user):
    """Updates UserOverdue fields without triggering email notification"""
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("daysUntil")
    appointmentsAttended = Appointment.objects.all().filter(patient=user).filter(noshow=False).order_by('appointment_start')  # get number of  attended appointments
    appointmentCount = countSeperateAppointments(appointmentsAttended)
    if appointmentCount == checkups.count() or Appointment.objects.all().filter(patient=user).filter(
            appointment_start__gte=timezone.now()).count() > 0:  # Finished study or already has upcoming appointment
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now() - timedelta(days=10)
        user.save()
        return
    nextCheckup = checkups[appointmentCount]
    user.next_checkup = user.date_joined + timedelta(days=nextCheckup.daysUntil)
    if (nextCheckup.daysUntil < days_since_joined):
        user.checkup_overdue = user.date_joined + timedelta(days=nextCheckup.daysUntil)
    else:
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now() - timedelta(days=10)
    user.save()


def checkAllUsersOverdue():
    patients = User.objects.filter(groups__name="Patient", )
    for p in patients:
        checkUserOverdue(p)


def doAppointmentReminders():
    appointmentsOneWeek = Appointment.objects.filter(taken=True, appointment_start__range=[timezone.now(), timezone.now() + timezone.timedelta(days=7)])
    appointmentsOneDay = Appointment.objects.filter(taken=True, appointment_start__range=[timezone.now(), timezone.now() + timezone.timedelta(hours=24)])

    for appointment in appointmentsOneDay:
        if not appointment.dayReminder:
            if sendDayReminderMail(appointment.patient) != -1:
                appointment.dayReminder = True

    for appointment in appointmentsOneWeek:
        if not appointment.weekReminder:
            if sendWeekReminderMail(appointment.patient) != -1:
                appointment.weekReminder = True
