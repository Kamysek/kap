import django_filters
import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay import from_global_id

from account.models import CustomUser
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
        fields = ['id', 'username', 'is_staff', 'is_active', 'date_joined']


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        is_staff = graphene.Boolean(required=True)
        is_active = graphene.Boolean(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            user_instance = get_user_model()(
                username=input.get('username'),
            )
            user_instance.set_password(input.get('password'))
            user_instance.save()
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

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                user_instance = CustomUser.objects.get(pk=from_global_id(input.get('id'))[1])
                if user_instance:
                    if input.get('password'):
                        user_instance.set_password(input.get('password'))
                    if input.get('is_staff'):
                        user_instance.is_staff = input.get('is_staff')
                    if input.get('is_active'):
                        user_instance.is_active = input.get('is_active')
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


class Query(graphene.AbstractType):
    get_user = graphene.relay.Node.Field(UserType)
    get_users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)

    get_group = graphene.relay.Node.Field(GroupType)
    get_groups = DjangoFilterConnectionField(GroupType, filterset_class=GroupFilter)

    get_user_group = graphene.String()

    @login_required
    def resolve_get_user_group(self, info, **kwargs):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            if info.context.user.groups.filter(name="Admin").exists():
                return "Admin"
            if info.context.user.groups.filter(name="Doctor").exists():
                return "Doctor"
            if info.context.user.groups.filter(name="Patient").exists():
                return "Patient"
        else:
            raise UnauthorisedAccessError(message='No permissions to view the user group!')


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()

    update_user = UpdateUser.Field()
    update_group = UpdateGroup.Field()

    delete_user = DeleteUser.Field()
