from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from appointments.models import Appointment
from django.contrib.auth.models import Group
from account.models import Checkup, Study


class Command(BaseCommand):
    help = 'Get a list of all permissions available in the system.'

    def handle(self, *args, **options):
        s = Study(name='Standard')
        s.save()
        c = Checkup(name="Initial checkup", daysUntil=0, study=s)
        c.save()
        c = Checkup(name="Six month checkup", daysUntil=30 * 6, study=s)
        c.save()
        c = Checkup(name="One year checkup", daysUntil=30 * 12, study=s)
        c.save()
        c = Checkup(name="1.5 year checkup", daysUntil=30 * 18, study=s)
        c.save()
        c = Checkup(name="2 year checkup", daysUntil=30 * 24, study=s)
        c.save()

        user1 = get_user_model().objects.create_user('kap', password='kap', email="kap@kap.com")
        user1.is_superuser = True
        user1.is_staff = True
        user1.save()
        my_group = Group.objects.get(name='Admin')
        my_group.user_set.add(user1)
        my_group = Group.objects.get(name='Doctor')
        my_group.user_set.add(user1)

        user2 = get_user_model().objects.create_user('001', password='test', email='user1@nowhere',
                                                     study_participation=s,
                                                     date_joined=timezone.now() - timedelta(days=10))
        user2.save()
        user3 = get_user_model().objects.create_user('002', password='test', email='user2@nowhere',
                                                     study_participation=s,
                                                     date_joined=timezone.now() - timedelta(days=20))
        user3.save()
        user4 = get_user_model().objects.create_user('003', password='test', email='user3@nowhere',
                                                     study_participation=s,
                                                     date_joined=timezone.now() - timedelta(days=30))
        user4.save()
        user5 = get_user_model().objects.create_user('004', password='test', email='user4@nowhere',
                                                     study_participation=s,
                                                     date_joined=timezone.now() - timedelta(days=40))
        user5.save()
        my_group = Group.objects.get(name='Patient')
        my_group.user_set.add(user2)
        my_group.user_set.add(user3)
        my_group.user_set.add(user4)
        my_group.user_set.add(user5)

        Appointment(title="Appointment 1", comment_doctor="Doc", comment_patient="Patient", patient=user4,
                    appointment_start=str(timezone.now().replace(hour=8, minute=0) - timedelta(days=29)),
                    appointment_end=str(
                        timezone.now().replace(hour=8, minute=0) - timedelta(days=29) + timedelta(minutes=30)),
                    taken=True).save()

        Appointment(title="Appointment 2", comment_doctor="Doc", comment_patient="Patient", patient=user5,
                    appointment_start=str(timezone.now().replace(hour=8, minute=0) - timedelta(days=29)),
                    appointment_end=str(
                        timezone.now().replace(hour=8, minute=0) - timedelta(days=29) + timedelta(minutes=30)),
                    taken=True).save()

        Appointment(title="Appointment 3", comment_doctor="Doc", comment_patient="Patient", patient=user2,
                    appointment_start=str(timezone.now().replace(hour=8, minute=0)),
                    appointment_end=str(
                        timezone.now().replace(hour=8, minute=0) + timedelta(minutes=30)),
                    taken=True).save()

        Appointment(title="Appointment 4", comment_doctor="Doc", comment_patient="Patient",
                    appointment_start=str(timezone.now().replace(hour=8, minute=0) + timedelta(days=30*6)),
                    appointment_end=str(
                        timezone.now().replace(hour=8, minute=0) + timedelta(minutes=30, days=30*6)),
                    taken=False).save()

        print("Successfully populated database with example data!")
