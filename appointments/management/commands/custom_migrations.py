"""
def set_permissions():
    # all permissions
    print("todo")
    group = Group.objects.get(name="Admin")
    somemodel_ct = ContentType.objects.get_for_model(Appointment)
    full_access = Permission(name='full access', codename='full_access', content_type=somemodel_ct)
    full_access.save()
    group.permissions.add(full_access)
"""
# backend/management/commands/initgroups.py
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from appointments.models import Appointment
from boards.models import Board,Post,Topic

GROUPS_PERMISSIONS = {
    'Admin': {
        Appointment: ['add', 'change', 'delete', 'view'],
        Board: ['add', 'change', 'delete', 'view'],
        Post: ['add', 'change', 'delete', 'view'],
        Topic: ['add', 'change', 'delete', 'view'],
    },
    'Doctor':{
        Appointment: ['add', 'change', 'delete', 'view'],
        Board: ['add', 'change', 'delete', 'view'],
        Post: ['add', 'change', 'delete', 'view'],
        Topic: ['add', 'change', 'delete', 'view'],
    },
    'Patient':{
        Appointment: ['view'],
        Board: ['view'],
        Post: ['view'],
        Topic: ['view'],
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