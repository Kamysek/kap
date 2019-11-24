from django.db import models
from django.contrib.auth import get_user_model


class Calendar(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    doctor = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("view_doctor", "View doctor"),
            ("edit_doctor", "Edit doctor"),
        )


class Appointment(models.Model):
    title = models.CharField(max_length=50, null=True)
    comment_doctor = models.TextField(max_length=500, null=False, blank=True, default="")
    comment_patient = models.TextField(max_length=500, null=False, blank=True, default="")
    calendar = models.ForeignKey(Calendar, null=True, blank=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)
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
            ("view_patient", "View patient"),
            ("edit_patient", "Edit patient"),
        )
