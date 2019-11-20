from django.db import models
from django.contrib.auth import get_user_model


class Calendar(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    title = models.CharField(max_length=50, null=True)
    comment_doctor = models.TextField(max_length=200, null=False, blank=True)
    comment_patient = models.TextField(max_length=200, null=False, blank=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    appointment_start = models.DateTimeField()
    appointment_end = models.DateTimeField()
    taken = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_add_appointment_patient", "Can add appointment patient"),
            ("can_change_appointment_patient", "Can change appointment patient"),
            ("can_delete_appointment_patient", "Can delete appointment patient"),
            ("can_view_appointment_patient", "Can view appointment patient"),
        )

