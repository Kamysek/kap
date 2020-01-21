from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from appointments.models import Appointment
from django.contrib.auth.models import Group
from account.models import Checkup,Study

class Command(BaseCommand):
    help = 'Get a list of all permissions available in the system.'

    def handle(self, *args, **options):
        s = Study(name='Standard')
        s.save()
        c = Checkup(name="First Checkup", daysUntil=-8, study=s)
        c.save()
        c = Checkup(name="2nd Checkup", daysUntil=360, study=s)
        c.save()
        c = Checkup(name="3rd Checkup", daysUntil=420, study=s)
        c.save()
        c = Checkup(name="4th Checkup", daysUntil=480, study=s)
        c.save()
        c = Checkup(name="5th Checkup", daysUntil=540, study=s)
        c.save()

        user1 = get_user_model().objects.create_user('kap', password='kap', email="kap@kap.com")
        user1.is_superuser = True
        user1.is_staff = True
        user1.save()
        my_group = Group.objects.get(name='Admin')
        my_group.user_set.add(user1)
        my_group = Group.objects.get(name='Doctor')
        my_group.user_set.add(user1)

        user2 = get_user_model().objects.create_user('TestPatient', password='patient', email='E.P.Riedel@gmail.com', study_participation=s)
        user2.save()
        my_group = Group.objects.get(name='Patient')
        my_group.user_set.add(user2)

        Appointment(title="Appointment 1", comment_doctor="Doc", comment_patient="Patient", patient=user1,
                    appointment_start=str(timezone.now()),
                    appointment_end=str(timezone.now() + timedelta(minutes=8)), taken=True).save()

        Appointment(title="Appointment 2", comment_doctor="Doc", comment_patient="Patient", patient=user1,
                    appointment_start=str(timezone.now() + timedelta(minutes=10)),
                    appointment_end=str(timezone.now() + timedelta(minutes=18)), taken=True).save()

        Appointment(title="Appointment 2.5", comment_doctor="Doc", comment_patient="Patient", patient=user1,appointment_start=str(timezone.now() + timedelta(minutes=50)),appointment_end=str(timezone.now() + timedelta(minutes=18)), taken=True).save()

        Appointment(title="Appointment 3", comment_doctor="Doc",
                    appointment_start=str(timezone.now() + timedelta(minutes=20)),
                    appointment_end=str(timezone.now() + timedelta(minutes=27)), taken=False).save()

        print("Successfully populated database with example data!")

