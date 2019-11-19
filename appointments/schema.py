import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import Appointment

def remove_sensitive_appointment(user, appointment):
    if user != appointment.patient:
        appointment.patient = None
        appointment.title = None
        appointment.comment = None
        appointment.files = None
        appointment.created_at = None
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
        if not info.context.user.is_authenticated:#TODO Check user group permissions
            return queryset
        remove_sensitive_data(info.context.user, queryset)
        return queryset


class CreateAppointment(graphene.Mutation):
    id = graphene.Int()
    timestamp = graphene.DateTime()

    class Arguments:
        title = graphene.String()
        comment = graphene.String()
        date = graphene.DateTime()

    @login_required
    def mutate(self, info, title, date, comment):
        appointment = Appointment(user=info.context.user, title=title, comment=comment, date=date)
        appointment.save()

        return CreateAppointment(
            id=appointment.id,
            timestamp=appointment.timestamp
        )


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
