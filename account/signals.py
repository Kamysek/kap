from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from account.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if sender.is_superuser:
            instance.groups.add(Group.objects.get(name='Admin'))
        else:
            instance.groups.add(Group.objects.get(name='Patient'))