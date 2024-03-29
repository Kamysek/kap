from django.db import models
from django.contrib.auth import get_user_model

from account.models import CustomUser
from django.utils import timezone


class Appointment(models.Model):
    title = models.CharField(max_length=50, null=True, blank=False)
    comment_doctor = models.TextField(max_length=500, null=True, blank=True, default="")
    comment_patient = models.TextField(max_length=500, null=True, blank=True, default="")
    patient = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    appointment_start = models.DateTimeField(null=True, blank=False)
    appointment_end = models.DateTimeField(null=True, blank=False)
    taken = models.BooleanField(null=True, blank=False, default=False)
    weekReminder = models.BooleanField(null=True, blank=False, default=False)
    dayReminder = models.BooleanField(null=True, blank=False, default=False)
    noshow = models.BooleanField(null=True, blank=False, default=False)

    def __str__(self):
        return self.title
