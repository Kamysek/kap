from django_cron import CronJobBase, Schedule
from appointments.models import Appointment
from django.utils import timezone
from datetime import timedelta
from klinischesanwendungsprojekt.mailUtils import sendOverdueMail,sendDayReminderMail,sendWeekReminderMail
from django.contrib.auth import get_user_model

User = get_user_model()

#TODO: Doesn't work if patient always books 2 time slots for whatever reason. TODO: Handle active Checkup
def checkUserOverdue(user):
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_start')
    days_since_joined = (timezone.now() - user.date_joined).days
    checkups = user.study_participation.checkup_set.all().order_by("daysUntil")
    #appointmentsFinished = Appointment.objects.all().filter(patient=user).filter(appointment_start__lte=timezone.now()).filter(noshow= False).count() #get number of PAST appointments that were actually attended
    appointmentsAttended = Appointment.objects.all().filter(patient=user).filter(noshow= False).count() #get number of  attended appointments
    print("attended apps: " + str(appointmentsAttended))
    if appointmentsAttended == checkups.count():#Finished study
        return
    nextCheckup = checkups[appointmentsAttended]
    print("days till next Checkup: " + str(nextCheckup))
    print("days since joined: " + str(days_since_joined))
    if (nextCheckup.daysUntil < days_since_joined):
        print("USER OVERDUE!")
        user.checkup_overdue = True
        if(days_since_joined-nextCheckup.daysUntil) > 3 and ((timezone.now() - user.overdue_notified) > timedelta(days=7)): #Notify if patient is more than 3 days overdue or last Notification is 1 week overdue
            sendOverdueMail(user,nextCheckup.name)
            user.overdue_notified = timezone.now()
    else:
        print("not overdue")
        user.checkup_overdue = False
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

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        doAppointmentReminders()
        checkAllUsersOverdue()
