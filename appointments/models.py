from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Calendar(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    title = models.CharField(max_length=50,null=True)
    comment = models.TextField(max_length=200,null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    appointment_at = models.DateTimeField()

    def __str__(self):
        return self.title
