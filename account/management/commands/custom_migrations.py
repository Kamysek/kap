# backend/management/commands/initgroups.py
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from appointments.models import Appointment
from account.models import CustomUser, Checkup, Study
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django_cron.models import CronJobLog
from survey.models import Survey, Question, Choice, Answer, TextAnswer, ChoiceAnswer, NumberAnswer

GROUPS_PERMISSIONS = {
    'Admin': {
        Group: ['add', 'change', 'delete', 'view'],
        Permission: ['add', 'change', 'delete', 'view'],
        ContentType: ['add', 'change', 'delete', 'view'],
        Session: ['add', 'change', 'delete', 'view'],
        LogEntry: ['add', 'change', 'delete', 'view'],

        CustomUser: ['add', 'change', 'delete', 'view'],
        Checkup: ['add', 'change', 'delete', 'view'],
        Study: ['add', 'change', 'delete', 'view'],
        CronJobLog: ['add', 'change', 'delete', 'view'],

        Appointment: ['add', 'change', 'delete', 'view'],

        Survey: ['add', 'change', 'delete', 'view'],
        Question: ['add', 'change', 'delete', 'view'],
        Choice: ['add', 'change', 'delete', 'view'],
        Answer: ['add', 'change', 'delete', 'view'],
        TextAnswer: ['add', 'change', 'delete', 'view'],
        ChoiceAnswer: ['add', 'change', 'delete', 'view'],
        NumberAnswer: ['add', 'change', 'delete', 'view'],

    },
    'Doctor': {
        CustomUser: ['add', 'change', 'delete', 'view'],
        Checkup: ['add', 'change', 'delete', 'view'],
        Study: ['add', 'change', 'delete', 'view'],
        CronJobLog: ['add', 'change', 'delete', 'view'],

        Appointment: ['add', 'change', 'delete', 'view'],

        Survey: ['add', 'change', 'delete', 'view'],
        Question: ['add', 'change', 'delete', 'view'],
        Choice: ['add', 'change', 'delete', 'view'],
        Answer: ['add', 'change', 'delete', 'view'],
        TextAnswer: ['add', 'change', 'delete', 'view'],
        ChoiceAnswer: ['add', 'change', 'delete', 'view'],
        NumberAnswer: ['add', 'change', 'delete', 'view'],
    },
    'Labor': {
        CustomUser: ['view'],
        Checkup: ['view'],
        Study: ['view'],
        CronJobLog: ['view'],

        Appointment: ['view'],

        Survey: ['view'],
        Question: ['view'],
        Choice: ['view'],
        Answer: ['view'],
        TextAnswer: ['view'],
        ChoiceAnswer: ['view'],
        NumberAnswer: ['view'],
    },
    'Patient': {
        Checkup: ['view'],
        Study: ['view'],
        CronJobLog: ['view'],

        Survey: ['view'],
        Question: ['view'],
        Choice: ['view'],
        Answer: ['add', 'change', 'delete'],
        TextAnswer: ['add', 'change', 'delete'],
        ChoiceAnswer: ['add', 'change', 'delete'],
        NumberAnswer: ['add', 'change', 'delete'],
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding "
                                          + codename
                                          + " to group "
                                          + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
