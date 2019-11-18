import graphene
from graphene_django import DjangoObjectType

from .models import Appointment


class AppointmentType(DjangoObjectType):
	class Meta:
		model = Appointment


class Query(graphene.ObjectType):
	appointments = graphene.List(AppointmentType)

	def resolve_appointments(self, info, **kwargs):
		return Appointment.objects.by_user(info)

class CreateAppointment(graphene.Mutation):
	#user =
	id = graphene.Int()
	timestamp = graphene.DateTime()

	class Arguments:
		title = graphene.String()
		comment = graphene.String()
		date = graphene.DateTime()

	def mutate(self, info, title,date, comment):
		appointment = Appointment(user=info.context.user,title=title, comment=comment,date=date)
		appointment.save()

		return CreateAppointment(
			id=appointment.id,
			timestamp=appointment.timestamp
        )


#4
class Mutation(graphene.ObjectType):
	create_appointment = CreateAppointment.Field()