from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from account.managers import CustomUserManager

class Study(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)

    def __str__(self):
        return self.name

class Checkup(models.Model):
    name = models.CharField(max_length=150,blank=False,null=True)
    order = models.IntegerField(null=True,blank=False)
    interval = models.IntegerField(null=True,blank=False)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150, null=True, blank=False)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=False)
    email_notification = models.BooleanField(default=False, null=True, blank=False)
    is_staff = models.BooleanField(default=False, null=True, blank=False)
    is_active = models.BooleanField(default=True, null=True, blank=False)
    date_joined = models.DateTimeField(default=timezone.now, null=True, blank=False)
    password_changed = models.BooleanField(default=False, null=True, blank=False)
    called = models.IntegerField(default=0, null=True, blank=False)
    study_participation = models.ForeignKey(Study,on_delete=models.SET_NULL,null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ("edit_user", "Edit user"),
        )

    def set_password(self, password):
        super(CustomUser, self).set_password(password)
        if self.date_joined < (timezone.now() - timedelta(seconds=3)):
            # So the password initialization doesnt automatically set this flag
            self.password_changed = True
