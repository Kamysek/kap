from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from appointments.models import Appointment, Calendar
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Get a list of all permissions available in the system.'

    def handle(self, *args, **options):
        user = get_user_model().objects.create_user('kap', password='kap')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        my_group = Group.objects.get(name='Admin')
        my_group.user_set.add(user)
        my_group = Group.objects.get(name='Doctor')
        my_group.user_set.add(user)


        user = get_user_model().objects.create_user('TestPatient', password='patient')
        user.save()
        my_group = Group.objects.get(name='Patient')
        my_group.user_set.add(user)

        Calendar(name="kapKalendar", doctor_id=1).save()
        Appointment(title="Appointment 1", comment_doctor="Doc", comment_patient="Patient", patient_id=1, calendar_id=1,
                    appointment_start=datetime.now(),
                    appointment_end=(datetime.now() + timedelta(minutes=8)), taken=True).save()

        Appointment(title="Appointment 2", comment_doctor="Doc", comment_patient="Patient", patient_id=2, calendar_id=1,
                    appointment_start=(datetime.now() + timedelta(minutes=10)),
                    appointment_end=(datetime.now() + timedelta(minutes=18)), taken=True).save()

        Appointment(title="Appointment 3", comment_doctor="Doc", calendar_id=1,
                    appointment_start=(datetime.now() + timedelta(minutes=10)),
                    appointment_end=(datetime.now() + timedelta(minutes=18)), taken=False).save()
