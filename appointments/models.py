from django.db import models
from django.conf import settings
from graphql import GraphQLError
from django.urls import reverse

User = settings.AUTH_USER_MODEL


def remove_sensitive_appointment(user, appointment):
	if user != appointment.user:
		appointment.user = None
		appointment.title = "anonym"
		appointment.comment = "anonym"
		appointment.files = 0
		#appointment.timestamp = "2019-11-18T10:39:40.461196+00:00"
		appointment.id = 0


def remove_sensitive_data(user, queryset):
	for appointment in queryset:
		remove_sensitive_appointment(user, appointment)

class RestrictManager(models.Manager):
	def by_user(self,info):
		queryset = super(RestrictManager,self).get_queryset()
		#print("removing sensitive Data from Entrys not by user: " + str(user))
		print(info.context.user.is_authenticated)
		if not info.context.user.is_authenticated:
			raise GraphQLError('You must be logged in to see this!')

		remove_sensitive_data(info.context.user,queryset)
		return queryset

class Appointment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	date = models.DateTimeField('Termin')
	comment = models.CharField(max_length=200)
	files = models.PositiveIntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	objects = RestrictManager()

	def __str__(self):
		return self.title