import django_filters
import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay import from_global_id
from account.models import CustomUser, Checkup, Study
from graphql_jwt.decorators import login_required


def hasGroup(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'password_changed']


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)
        fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'password_changed', 'study_participation')

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.id
        else:
            raise UnauthorisedAccessError(message='Unauthorized')
            return None

    @login_required
    def resolve_username(self, info):
        if hasGroup(["Admin", "Doctor", "Labor"], info) or self == info.context.user:
            return self.username
        return None

    @login_required
    def resolve_password(self, info):
        if self == info.context.user:
            return self.password
        return None

    @login_required
    def resolve_email(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info) or self == info.context.user:
            return self.email
        return None

    @login_required
    def resolve_email_notification(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info) or self == info.context.user:
            return self.email_notification
        return None

    @login_required
    def resolve_is_staff(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info) or self == info.context.user:
            return self.is_staff
        return None

    @login_required
    def resolve_is_active(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info) or self == info.context.user:
            return self.is_active
        return None

    @login_required
    def resolve_date_joined(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self == info.context.user:
            return self.date_joined
        return None

    @login_required
    def resolve_password_changed(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self == info.context.user:
            return self.password_changed
        return None

    @login_required
    def resolve_called(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info) or self == info.context.user:
            return self.called
        return None


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        is_staff = graphene.Boolean(required=True)
        is_active = graphene.Boolean(required=True)
        group = graphene.String(required=False)
        email_notification = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            user_instance = get_user_model()(
                username=input.get('username'),
                email=input.get('email'),
                is_staff=input.get('is_staff'),
                is_active=input.get('is_active'),
                email_notification=input.get('email_notification'),
            )
            user_instance.set_password(input.get('password'))
            user_instance.save()

            if input.get('group') == "Admin" and not hasGroup(["Admin"], info):
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
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()
        add_group = graphene.String()
        remove_group = graphene.String()
        email = graphene.String()
        email_notification = graphene.Boolean()
        called = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                user_instance = CustomUser.objects.get(pk=from_global_id(input.get('id'))[1])
                if user_instance:
                    if input.get('password'):
                        user_instance.set_password(input.get('password'))
                    if input.get('email'):
                        user_instance.email = input.get('password')
                    if input.get('is_staff'):
                        user_instance.is_staff = input.get('is_staff')
                    if input.get('is_active'):
                        user_instance.is_active = input.get('is_active')
                    if input.get('email_notification'):
                        user_instance.email_notification = input.get('email_notification')
                    if input.get('called'):
                        user_instance.called += 1
                    if input.get('add_group'):
                        if input.get('add_group') == "Admin" and not hasGroup(["Admin"], info):
                            raise UnauthorisedAccessError(message='Must be Admin to create Admin')
                        Group.objects.get(name=input.get('add_group')).user_set.add(user_instance)
                    if input.get('remove_group'):
                        if input.get('remove_group') == "Admin" and not hasGroup(["Admin"], info):
                            raise UnauthorisedAccessError(message='Must be Admin to remove Admin')
                        Group.objects.get(name=input.get('removegroup')).user_set.remove(user_instance)
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
        if hasGroup(["Admin", "Doctor"], info):
            try:
                user_instance = CustomUser.objects.get(pk=from_global_id(input.get('id'))[1])
                if user_instance:
                    user_instance.delete()
                    return DeleteUser(ok=True)
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a user!')


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['id']


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        interfaces = (graphene.relay.Node,)


class CreateGroup(graphene.relay.ClientIDMutation):
    group = graphene.Field(GroupType)

    class Input:
        name = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin"], info):
            group_instance = Group.objects.get_or_create(name=input.get('name'))
            group_instance.save()
            return CreateGroup(group=group_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a group!')


class UpdateGroup(graphene.relay.ClientIDMutation):
    class Input:
        group_str = graphene.String()
        user_id = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin"], info):
            try:
                user_instance = CustomUser.objects.get(pk=from_global_id(input.get('user_id'))[1])
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')

            try:
                group_instance = Group.objects.get(name=from_global_id(input.get('group_str'))[1])
            except Group.DoesNotExist:
                raise GraphQLError('Group does not exist!')

            user_instance.groups.add(group_instance)

            return UpdateGroup(group_str=group_instance.name, user_id=user_instance.id)
        else:
            raise UnauthorisedAccessError(message='No permissions to update a group!')


class StudyFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = ['name']


class StudyType(DjangoObjectType):
    class Meta:
        model = Study
        interfaces = (graphene.relay.Node,)
        fields = ('name', 'customuser_set', 'checkup_set')

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.id
        else:
            raise UnauthorisedAccessError(message='Unauthorized')
            return None

    @login_required
    def resolve_name(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.name
        return None

    @login_required
    def resolve_customuser_set(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.customuser_set
        return []

    @login_required
    def resolve_checkup_set(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.checkup_set
        return []


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
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.id
        else:
            raise UnauthorisedAccessError(message='Unauthorized')
            return None

    @login_required
    def resolve_name(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.name
        return None

    @login_required
    def resolve_order(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.order
        return None

    @login_required
    def resolve_interval(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.interval
        return None

    @login_required
    def resolve_study(self, info):
        if hasGroup(["Admin", "Doctor",  "Labor"], info):
            return self.study
        return None


class Query(graphene.AbstractType):
    get_user = graphene.relay.Node.Field(UserType)
    get_users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    get_me = graphene.Field(UserType)

    get_checkup = graphene.relay.Node.Field(CheckupType)
    get_studies = DjangoFilterConnectionField(StudyType, filterset_class=StudyFilter)

    get_group = graphene.relay.Node.Field(GroupType)
    get_groups = DjangoFilterConnectionField(GroupType, filterset_class=GroupFilter)

    get_user_group = graphene.String()

    @login_required
    def resolve_get_user_group(self, info, **kwargs):
        if hasGroup(["Admin", "Doctor",  "Labor", "Patient"], info):
            if info.context.user.groups.filter(name="Admin").exists():
                return "Admin"
            if info.context.user.groups.filter(name="Doctor").exists():
                return "Doctor"
            if info.context.user.groups.filter(name="Labor").exists():
                return "Labor"
            if info.context.user.groups.filter(name="Patient").exists():
                return "Patient"
        else:
            raise UnauthorisedAccessError(message='No permissions to view the user group!')

    @login_required
    def resolve_get_me(self, info, **kwargs):
        if hasGroup(["Admin", "Doctor",  "Labor", "Patient"], info):
            return info.context.user
        else:
            raise UnauthorisedAccessError(message='No permissions to view the user group!')


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()

    update_user = UpdateUser.Field()
    update_group = UpdateGroup.Field()

    delete_user = DeleteUser.Field()
