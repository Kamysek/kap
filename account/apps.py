from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountConfig(AppConfig):
    name = 'account'
"""
    def ready(self):
        from account.signals import init_groups
        post_migrate.connect(init_groups, sender=self)
"""