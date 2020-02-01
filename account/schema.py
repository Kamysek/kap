from datetime import timedelta
from django.utils import timezone
import django_filters
import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from account.models import CustomUser, Checkup, Study, Call
from graphql_jwt.decorators import login_required
from appointments.models import Appointment
from utils.HelperMethods import valid_id, has_group, UnauthorisedAccessError, countSeperateAppointments


class CallFilter(django_filters.FilterSet):
    class Meta:
        model = Call
        fields = ['date', 'comment', 'user']


class CallType(DjangoObjectType):

    class Meta:
        model = Call
        interfaces = (graphene.relay.Node,)
        fields = ('date', 'comment', 'user')

    @login_required
    def resolve_id(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.id
        return None

    @login_required
    def resolve_date(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self.user == info.context.user:
            return self.date
        return None

    @login_required
    def resolve_comment(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self.user == info.context.user:
            return self.comment
        return None

    @login_required
    def resolve_user(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self.user == info.context.user:
            return self.user
        return None


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'email_notification', 'is_staff', 'is_active', 'date_joined', 'password_changed',
                  'study_participation', 'overdue_notified', 'timeslots_needed']


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)
        fields = (
            'username', 'email', 'email_notification', 'is_staff', 'is_active', 'date_joined', 'password_changed',
            'study_participation', 'overdue_notified', 'timeslots_needed', 'call_set')

    @login_required
    def resolve_id(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.id
        return None

    @login_required
    def resolve_username(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.username
        return None

    @login_required
    def resolve_email(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.email
        return None

    @login_required
    def resolve_email_notification(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.email_notification
        return None

    @login_required
    def resolve_password(self, info):
        if self == info.context.user:
            return self.password
        return None

    @login_required
    def resolve_is_staff(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.is_staff
        return None

    @login_required
    def resolve_is_active(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.is_active
        return None

    @login_required
    def resolve_date_joined(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.date_joined
        return None

    @login_required
    def resolve_password_changed(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.password_changed
        return None

    @login_required
    def resolve_study_participation(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.study_participation
        return None

    @login_required
    def resolve_checkup_overdue(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.checkup_overdue
        return None

    @login_required
    def resolve_overdue_notified(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.overdue_notified
        return None

    @login_required
    def resolve_timeslots_needed(self, info):
        if has_group(["Admin", "Doctor"], info) or self == info.context.user:
            return self.timeslots_needed
        return None

    @login_required
    def resolve_call_set(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.call_set
        return []


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        is_staff = graphene.Boolean(required=True)
        is_active = graphene.Boolean(required=True)
        group = graphene.String(required=True)
        timeslots_needed = graphene.Int()
        study_participation = graphene.ID()
        email_notification = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin"], info):

            study_instance = Study.objects.get(pk=valid_id(input.get('study_participation'), StudyType)[1])

            user_instance = get_user_model()(
                username=input.get('username'),
                email=input.get('email'),
                is_staff=input.get('is_staff'),
                is_active=input.get('is_active'),
                timeslots_needed=input.get('timeslots_needed') if input.get('timeslots_needed') else 1,
                study_participation=study_instance if study_instance else None,
                email_notification=input.get('email_notification') if input.get('email_notification') else True,
            )
            user_instance.set_password(input.get('password'))
            user_instance.save()

            if input.get('group') == "Admin" and not has_group(["Admin"], info):
                raise UnauthorisedAccessError(message='Must be Admin to create Admin')
            Group.objects.get(name=input.get('group')).add(user_instance)

            return CreateUser(user=user_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a user!')


class UpdateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID(required=True)
        password = graphene.String()
        email = graphene.String()
        email_notification = graphene.Boolean()
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        study_participation = graphene.ID()
        timeslots_needed = graphene.Int()
        add_group = graphene.String()
        remove_group = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            try:
                user_instance = CustomUser.objects.get(pk=valid_id(input.get('id'), UserType)[1])
                if user_instance:
                    if input.get('password'):
                        user_instance.set_password(input.get('password'))
                    if input.get('email'):
                        user_instance.email = input.get('email')
                    if input.get('email_notification'):
                        user_instance.email_notification = input.get('email_notification')
                    if input.get('is_staff'):
                        user_instance.is_staff = input.get('is_staff')
                    if input.get('is_active'):
                        user_instance.is_active = input.get('is_active')
                    if input.get('study_participation'):
                        user_instance.is_active = input.get('study_participation')
                    if input.get('timeslots_needed'):
                        user_instance.is_active = input.get('timeslots_needed')
                    if input.get('add_group'):
                        if input.get('add_group') == "Admin" and not has_group(["Admin"], info):
                            raise UnauthorisedAccessError(message='Must be Admin to create Admin')
                        Group.objects.get(name=input.get('add_group')).user_set.add(user_instance)
                    if input.get('remove_group'):
                        if input.get('remove_group') == "Admin" and not has_group(["Admin"], info):
                            raise UnauthorisedAccessError(message='Must be Admin to remove Admin')
                        Group.objects.get(name=input.get('removegroup')).user_set.remove(user_instance)
                    user_instance.save()
                    return UpdateUser(user=user_instance)
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
        elif has_group(["Patient"], info):
            try:
                user_instance = CustomUser.objects.get(pk=valid_id(input.get('id'), UserType)[1])
                if user_instance:
                    if input.get('password'):
                        user_instance.set_password(input.get('password'))
                    if input.get('email'):
                        user_instance.email = input.get('email')
                    user_instance.save()
                    return UpdateUser(user=user_instance)
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a user!')


class DeleteUser(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin"], info):
            try:
                user_instance = CustomUser.objects.get(pk=valid_id(input.get('id'), UserType)[1])
                if user_instance:
                    user_instance.delete()
                    return DeleteUser(ok=True)
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a user!')


class UserCalled(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        user_id = graphene.ID(required=True)
        comment = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor", "Labor"], info):
            try:
                user_instance = CustomUser.objects.get(pk=valid_id(input.get('user_id'), CustomUser)[1])
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
            if input.get('comment'):
                Call(date=timezone.now(), comment=input.get('comment'), user=user_instance).save()
            return UserCalled(user=user_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to update user called field!')


class StudyFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = ['id', 'name']


class StudyType(DjangoObjectType):
    class Meta:
        model = Study
        interfaces = (graphene.relay.Node,)
        fields = ('name', 'customuser_set', 'checkup_set')

    @login_required
    def resolve_id(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.id
        return None

    @login_required
    def resolve_name(self, info):
        if has_group(["Patient", "Admin", "Doctor", "Labor"], info):
            return self.name
        return None

    @login_required
    def resolve_customuser_set(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.customuser_set
        return []

    @login_required
    def resolve_checkup_set(self, info):
        if has_group(["Patient", "Admin", "Doctor", "Labor"], info):
            return self.checkup_set
        return []


class CreateStudy(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    study = graphene.Field(StudyType)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            if input.get("name") and len(input.get("name")) != 0:
                study_instance = Study(name=input.get("name"))
                study_instance.save()
                return CreateStudy(study=study_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a study!')


class UpdateStudy(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    study = graphene.Field(StudyType)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            if input.get("name") and len(input.get("name")) != 0 and input.get("id"):

                study_instance = Study.objects.get(pk=valid_id(input.get('id'), StudyType)[1])

                if study_instance:
                    study_instance.name = input.get("name")
                    study_instance.save()
                    return UpdateStudy(study=study_instance)
                else:
                    raise GraphQLError("No study with this ID found")
        else:
            raise UnauthorisedAccessError(message='No permissions to update study!')


class DeleteStudy(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            if input.get("id"):
                study_instance = Study.objects.get(pk=valid_id(input.get('id'), StudyType)[1])
                if study_instance:
                    study_instance.delete()
                    return DeleteStudy(ok=True)
                else:
                    raise GraphQLError("No study with this ID found")
            else:
                raise GraphQLError("No study with this ID found")
        else:
            raise UnauthorisedAccessError(message='No permissions to delete study!')


class CheckupFilter(django_filters.FilterSet):
    class Meta:
        model = Checkup
        fields = ['name', 'daysUntil', 'study']


class CheckupType(DjangoObjectType):
    class Meta:
        model = Checkup
        interfaces = (graphene.relay.Node,)
        fields = ('name', 'daysUntil', 'study')

    @login_required
    def resolve_id(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.id
        return None

    @login_required
    def resolve_name(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.name
        return None

    @login_required
    def resolve_daysUntil(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.daysUntil
        return None

    @login_required
    def resolve_study(self, info):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return self.study
        return None


class CreateCheckup(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        study_id = graphene.ID(required=True)
        daysUntil = graphene.Int(required=True)

    checkup = graphene.Field(CheckupType)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            if input.get("name") and len(input.get("name")) != 0 and input.get("study_id") and input.get("daysUntil"):
                study_instance = Study.objects.get(pk=valid_id(input.get('study_id'), StudyType)[1])
                if study_instance:
                    checkup_instance = Checkup(name=input.get("name"), daysUntil=input.get("daysUntil"),
                                               study=study_instance)
                    checkup_instance.save()
                    return CreateCheckup(checkup=checkup_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a checkup!')


class UpdateCheckup(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String()
        id = graphene.ID(required=True)
        daysUntil = graphene.Int()

    checkup = graphene.Field(CheckupType)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            checkup_instance = Checkup.objects.get(pk=valid_id(input.get('id'), CheckupType)[1])
            if checkup_instance:
                if input.get("daysUntil"):
                    checkup_instance.daysUntil = input.get("daysUntil")
                if input.get("name"):
                    checkup_instance.name = input.get("name")
                checkup_instance.save()
                return UpdateCheckup(checkup=checkup_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to update checkup!')


class DeleteCheckup(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if has_group(["Admin", "Doctor"], info):
            checkup_instance = Checkup.objects.get(pk=valid_id(input.get('id'), CheckupType)[1])
            if checkup_instance:
                checkup_instance.delete()
                return DeleteCheckup(ok=True)
        else:
            raise UnauthorisedAccessError(message='No permissions to delete checkup!')


class Query(graphene.AbstractType):

    get_user = graphene.relay.Node.Field(UserType)
    get_users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    get_me = graphene.Field(UserType)

    get_checkup = graphene.relay.Node.Field(CheckupType)
    get_studies = DjangoFilterConnectionField(StudyType, filterset_class=StudyFilter)

    get_overdue_patients = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    get_user_group = graphene.String()

    get_checkup_date = graphene.DateTime()

    @login_required
    def resolve_get_overdue_patients(self, info, **kwargs):
        if has_group(["Admin", "Doctor", "Labor"], info):
            return CustomUser.objects.filter(groups__name="Patient", checkup_overdue__isnull=False)
        return None

    @login_required
    def resolve_get_user_group(self, info, **kwargs):
        if has_group(["Admin", "Doctor", "Labor", "Patient"], info):
            if info.context.user.groups.filter(name="Admin").exists():
                return "Admin"
            if info.context.user.groups.filter(name="Doctor").exists():
                return "Doctor"
            if info.context.user.groups.filter(name="Labor").exists():
                return "Labor"
            if info.context.user.groups.filter(name="Patient").exists():
                return "Patient"
        return None

    @login_required
    def resolve_get_me(self, info, **kwargs):
        if has_group(["Admin", "Doctor", "Labor", "Patient"], info):
            return info.context.user
        return None

    @login_required
    def resolve_get_checkup_date(self, info, **kwargs):
        if has_group(["Admin", "Doctor", "Labor", "Patient"], info):
            try:
                checkups = info.context.user.study_participation.checkup_set.all().order_by("daysUntil")
                appointmentsAttended = Appointment.objects.all().filter(patient=info.context.user).filter(
                    noshow=False).order_by(
                    'appointment_start')  # get number of  attended appointments
                appointmentCount = countSeperateAppointments(appointmentsAttended)
                nextCheckup = checkups[appointmentCount]
                date = info.context.user.date_joined + timedelta(days=nextCheckup.daysUntil)
            except:
                raise GraphQLError(message="User does not have study participation!")
            return date
        return None


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()

    update_user = UpdateUser.Field()

    user_called = UserCalled.Field()

    delete_user = DeleteUser.Field()


    create_study = CreateStudy.Field()
    update_study = UpdateStudy.Field()
    delete_study = DeleteStudy.Field()

    create_checkup = CreateCheckup.Field()
    update_checkup = UpdateCheckup.Field()
    delete_checkup = DeleteCheckup.Field()
