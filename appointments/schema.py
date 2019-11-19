import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import Appointment


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

class AppointmentType(DjangoObjectType):
	class Meta:
		model = Appointment


class Query(graphene.ObjectType):
	appointments = graphene.List(AppointmentType)
	@login_required
	def resolve_appointments(self, info, **kwargs):
		queryset = Appointment.objects.all()
		if not info.context.user.is_authenticated:
			raise GraphQLError('You must be logged in to see this!')
		remove_sensitive_data(info.context.user,queryset)
		return queryset
		return Appointment.objects.by_user(info)


class CreateAppointment(graphene.Mutation):
	id = graphene.Int()
	timestamp = graphene.DateTime()

	class Arguments:
		title = graphene.String()
		comment = graphene.String()
		date = graphene.DateTime()
	@login_required
	def mutate(self, info, title,date, comment):
		appointment = Appointment(user=info.context.user,title=title, comment=comment,date=date)
		appointment.save()

		return CreateAppointment(
			id=appointment.id,
			timestamp=appointment.timestamp
		)


class Mutation(graphene.ObjectType):
	create_appointment = CreateAppointment.Field()
