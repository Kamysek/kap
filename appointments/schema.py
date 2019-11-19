import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .models import Appointment, Calendar

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
        if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(name='Admin').exists():
            return queryset
        else:
            remove_sensitive_data(info.context.user, queryset)
            return queryset


class CreateAppointment(graphene.Mutation):
    id = graphene.Int()
    created_at = graphene.DateTime()

    class Arguments:
        title = graphene.String()
        comment = graphene.String()
        appointment_at = graphene.DateTime()
        calendar = graphene.String()

    @login_required
    def mutate(self, info, title, appointment_at, comment, calendar):
        appointment = Appointment(patient=info.context.user, title=title, comment=comment, appointment_at=appointment_at, calendar=Calendar.objects.get(name=calendar))
        appointment.save()

        return CreateAppointment(
            id=appointment.id,
            created_at=appointment.created_at
        )


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
