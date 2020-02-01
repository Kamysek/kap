from django_cron import CronJobBase, Schedule
from appointments.models import Appointment
from django.utils import timezone
from datetime import timedelta
from utils.mailUtils import sendOverdueMail,sendDayReminderMail,sendWeekReminderMail
from django.contrib.auth import get_user_model

User = get_user_model()


# return number of appointments that take place on seperate days to ignore double slots
# Input HAS TO BE appointment list sorted by date
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
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_start')
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("daysUntil")
    # appointmentsFinished = Appointment.objects.all().filter(patient=user).filter(appointment_start__lte=timezone.now()).filter(noshow= False).count() #get number of PAST appointments that were actually attended
    appointmentsAttended = Appointment.objects.all().filter(patient=user).filter(noshow= False).order_by('appointment_start')# get number of  attended appointments
    appointmentCount= countSeperateAppointments(appointmentsAttended)
    if appointmentCount == checkups.count() or Appointment.objects.all().filter(patient=user).filter(appointment_start__gte=timezone.now()).count() > 0:# Finished study or already has upcoming appointment
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now()
        user.save()
        return
    nextCheckup = checkups[appointmentCount]
    if (nextCheckup.daysUntil < days_since_joined):
        user.checkup_overdue = user.date_joined + timedelta(days=nextCheckup.daysUntil)
        if(days_since_joined-nextCheckup.daysUntil) > 3 and ((timezone.now() - user.overdue_notified) > timedelta(days=7)): # Notify if patient is more than 3 days overdue or last Notification is 1 week overdue
            sendOverdueMail(user,nextCheckup.name)
            user.overdue_notified = timezone.now()
    else:
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now()
    user.save()


def updateUserOverdue(user):#Updates UserOverdue fields without triggering email notification bc. of faster response
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_start')
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("daysUntil")
    appointmentsAttended = Appointment.objects.all().filter(patient=user).filter(noshow= False).order_by('appointment_start')# get number of  attended appointments
    appointmentCount= countSeperateAppointments(appointmentsAttended)
    if appointmentCount == checkups.count() or Appointment.objects.all().filter(patient=user).filter(appointment_start__gte=timezone.now()).count() > 0:# Finished study or already has upcoming appointment
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now()
        user.save()
        return
    nextCheckup = checkups[appointmentCount]
    if (nextCheckup.daysUntil < days_since_joined):
        user.checkup_overdue = user.date_joined + timedelta(days=nextCheckup.daysUntil)
    else:
        user.checkup_overdue = None;
        user.overdue_notified = timezone.now()
    user.save()


def checkAllUsersOverdue():
    patients = User.objects.filter(groups__name="Patient",)
    for p in patients:
        checkUserOverdue(p)


def doAppointmentReminders():
    appointmentsOneWeek = Appointment.objects.filter(taken=True,appointment_start__range=[timezone.now(),timezone.now()+timezone.timedelta(days=7)])
    appointmentsOneDay = Appointment.objects.filter(taken=True,appointment_start__range=[timezone.now(),timezone.now()+timezone.timedelta(hours=24)])

    for appointment in appointmentsOneDay:
        if not appointment.dayReminder:
            sendDayReminderMail(appointment.patient)
            appointment.dayReminder = True

    for appointment in appointmentsOneWeek:
        if not appointment.weekReminder:
            sendWeekReminderMail(appointment.patient)
            appointment.weekReminder = True


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 360 # every 6 hours
    RUN_AT_TIMES = ['1:00', '12:30']

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        doAppointmentReminders()
        checkAllUsersOverdue()
