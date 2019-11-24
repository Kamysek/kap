from django.db import models
from django.contrib.auth import get_user_model


class Calendar(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    doctor_id = models.PositiveIntegerField(null=False,blank=False)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    title = models.CharField(max_length=50, null=True)
    comment_doctor = models.TextField(max_length=500, null=False, blank=True, default="")
    comment_patient = models.TextField(max_length=500, null=False, blank=True, default="")
    calendar_id = models.PositiveIntegerField(null=False, blank=False)
    patient_id = models.PositiveIntegerField(null=True, blank=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    appointment_start = models.DateTimeField()
    appointment_end = models.DateTimeField()
    taken = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("add_appointment_patient", "Add appointment patient"),
            ("change_appointment_patient", "Change appointment patient"),
            ("delete_appointment_patient", "Delete appointment patient"),
            ("view_appointment_patient", "View appointment patient"),
        )
