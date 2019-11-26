# backend/management/commands/initgroups.py
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from appointments.models import Appointment, Calendar
from boards.models import Board, Post, Topic
from account.models import CustomUser
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from survey.models import Survey, Question, Choice, Answer, TextAnswer, ChoiceAnswer, NumberAnswer

GROUPS_PERMISSIONS = {
    'Admin': {
        Group: ['add', 'change', 'delete', 'view'],
        Permission: ['add', 'change', 'delete', 'view'],
        ContentType: ['add', 'change', 'delete', 'view'],
        Session: ['add', 'change', 'delete', 'view'],
        LogEntry: ['add', 'change', 'delete', 'view'],

        CustomUser: ['add', 'change', 'delete', 'view'],

        Board: ['add', 'change', 'delete', 'view'],
        Post: ['add', 'change', 'delete', 'view'],
        Topic: ['add', 'change', 'delete', 'view'],

        Calendar: ['add', 'change', 'delete', 'view'],
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

        Board: ['add', 'change', 'delete', 'view'],
        Post: ['add', 'change', 'delete', 'view'],
        Topic: ['add', 'change', 'delete', 'view'],

        Calendar: ['add', 'change', 'delete', 'view'],
        Appointment: ['add', 'change', 'delete', 'view'],

        Survey: ['add', 'change', 'delete', 'view'],
        Question: ['add', 'change', 'delete', 'view'],
        Choice: ['add', 'change', 'delete', 'view'],
        Answer: ['add', 'change', 'delete', 'view'],
        TextAnswer: ['add', 'change', 'delete', 'view'],
        ChoiceAnswer: ['add', 'change', 'delete', 'view'],
        NumberAnswer: ['add', 'change', 'delete', 'view'],
    },
    'Patient': {
        Board: ['view'],
        Post: ['view'],
        Topic: ['view'],

        Calendar: ['view'],

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

    # add custom permissions
        proj_add_perm1 = Permission.objects.get(name='Add appointment patient')
        proj_add_perm2 = Permission.objects.get(name='Change appointment patient')
        proj_add_perm3 = Permission.objects.get(name='Delete appointment patient')
        proj_add_perm4 = Permission.objects.get(name='View appointment patient')
        proj_add_perm5 = Permission.objects.get(name='View patient')
        proj_add_perm6 = Permission.objects.get(name='View comment doctor')
        proj_add_perm7 = Permission.objects.get(name='View doctor')

        proj_add_perm8 = Permission.objects.get(name='Edit user')

        proj_add_perm9 = Permission.objects.get(name='View board creator')
        proj_add_perm10 = Permission.objects.get(name='View topic creator')
        proj_add_perm11 = Permission.objects.get(name='View created by Board')
        proj_add_perm12 = Permission.objects.get(name='View updated by Board')

        proj_add_perm13 = Permission.objects.get(name='View created by Survey')
        proj_add_perm14 = Permission.objects.get(name='View updated by Survey')
        proj_add_perm15 = Permission.objects.get(name='View text answer')
        proj_add_perm16 = Permission.objects.get(name='View choice answer')
        proj_add_perm17 = Permission.objects.get(name='View number answer')

        Group.objects.get(name='Admin').permissions.add(proj_add_perm1)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm2)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm3)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm4)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm5)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm6)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm7)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm8)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm9)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm10)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm11)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm12)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm13)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm14)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm15)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm16)
        Group.objects.get(name='Admin').permissions.add(proj_add_perm17)

        Group.objects.get(name='Doctor').permissions.add(proj_add_perm5)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm6)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm7)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm9)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm10)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm11)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm12)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm13)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm14)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm15)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm16)
        Group.objects.get(name='Doctor').permissions.add(proj_add_perm17)

        Group.objects.get(name='Patient').permissions.add(proj_add_perm1)
        Group.objects.get(name='Patient').permissions.add(proj_add_perm2)
        Group.objects.get(name='Patient').permissions.add(proj_add_perm3)
        Group.objects.get(name='Patient').permissions.add(proj_add_perm4)
