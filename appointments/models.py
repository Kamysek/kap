from django.db import models
from django.conf import settings
from graphql import GraphQLError
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Appointment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	date = models.DateTimeField('Termin')
	comment = models.CharField(max_length=200)
	files = models.PositiveIntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __str__(self):
		return self.title