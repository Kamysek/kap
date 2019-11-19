from django.db import models
from django.contrib.auth import get_user_model


class Calendar(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Appointment(models.Model):
    title = models.CharField(max_length=50)
    comment = models.TextField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_at = models.DateTimeField()