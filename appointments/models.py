from django.db import models
from django.contrib.auth import get_user_model


class Calendar(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)
    doctor = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    title = models.CharField(max_length=50, null=True, blank=False)
    comment_doctor = models.TextField(max_length=500, null=True, blank=True, default="")
    comment_patient = models.TextField(max_length=500, null=True, blank=True, default="")
    calendar = models.ForeignKey(Calendar, null=True, blank=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    appointment_start = models.DateTimeField(null=True, blank=False)
    appointment_end = models.DateTimeField(null=True, blank=False)
    taken = models.BooleanField(null=True, blank=False, default=False)

    def __str__(self):
        return self.title
