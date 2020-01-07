from django_cron import CronJobBase, Schedule
from appointments.models import Appointment
from django.utils import timezone
from klinischesanwendungsprojekt.mailUtils import sendOverdueMail,sendDayReminderMail,sendWeekReminderMail
from django.contrib.auth import get_user_model

User = get_user_model()


def checkUserOverdue(user):
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_start')
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("order")
    totalDaysNextCheckup = 0
    for i in range(appointments.count() + 1):
        totalDaysNextCheckup += checkups[i].interval
    if (days_since_joined > totalDaysNextCheckup):
        user.checkup_overdue = True
        if(days_since_joined - totalDaysNextCheckup) > 3 and not user.overdue_notified:
            sendOverdueMail(user)
            user.overdue_notified = True
    else:
        user.checkup_overdue = False
        user.overdue_notified = False
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

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        doAppointmentReminders()
        checkAllUsersOverdue()
