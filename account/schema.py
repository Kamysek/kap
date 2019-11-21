import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from account.models import CustomUser
from graphql_jwt.decorators import login_required


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    password = graphene.String()
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('account.can_add_custom_user'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                user_instance = get_user_model()(
                    username=input.username,
                )
                user_instance.set_password(input.password)
                user_instance.save()
                return CreateUser(user=user_instance)
            else:
                raise UnauthorisedAccessError(message='No permissions to create user!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a user!')


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_id, input=None):
        if info.context.user.has_perm('account.can_change_custom_user'):
            try:
                user_instance = CustomUser.objects.get(pk=user_id)
                if user_instance:
                    if input.password:
                        user_instance.password = input.password
                    if input.is_staff:
                        user_instance.is_staff = input.is_staff
                    if input.is_active:
                        user_instance.is_active = input.is_active
                    user_instance.save()
                    return UpdateUser(user=user_instance)
            except CustomUser.DoesNotExist:
                raise GraphQLError('User does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a user!')


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        user_id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_id):
        if info.context.user.has_perm('account.can_delete_custom_user'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                try:
                    user_instance = CustomUser.objects.get(pk=user_id)
                    if user_instance:
                        user_instance.delete()
                        return DeleteUser(ok=True)
                except CustomUser.DoesNotExist:
                    raise GraphQLError('User does not exist!')
            else:
                raise UnauthorisedAccessError(message='No permissions to delete user!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a user!')


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class GroupInput(graphene.InputObjectType):
    name = graphene.String()


class CreateGroup(graphene.Mutation):
    class Arguments:
        input = GroupInput(required=True)

    group = graphene.Field(GroupType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('auth.can_add_group'):
            if info.context.user.groups.filter(name='Admin').exists():
                group_instance = Group.objects.get_or_create(name=input.name)
                group_instance.save()

                return CreateGroup(group=group_instance)
            else:
                raise UnauthorisedAccessError(message='No permissions to create the group!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a group!')


class UpdateGroup(graphene.Mutation):
    group_str = graphene.String()
    user_id = graphene.Int()

    class Arguments:
        group_str = graphene.String()
        user_id = graphene.Int()

    @login_required
    def mutate(self, info, group_str, user_id):
        if info.context.user.has_perm('auth.can_update_group'):
            if info.context.user.groups.filter(name='Admin').exists():
                try:
                    user_instance = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    raise GraphQLError('User does not exist!')

                try:
                    group_instance = Group.objects.get(name=group_str)
                except Group.DoesNotExist:
                    raise GraphQLError('Group does not exist!')

                user_instance.groups.add(group_instance)

                return UpdateGroup(group_str=group_instance.name, user_id=user_instance.id)
            else:
                raise UnauthorisedAccessError(message='No permissions to update the group!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a group!')


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    group = graphene.Field(GroupType)
    groups = graphene.List(GroupType)

    @login_required
    def resolve_me(self, info, **kwargs):
        if info.context.user.has_perm('account.can_view_custom_user'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                user = info.context.user
                if user.is_anonymous:
                    raise GraphQLError('Not logged in!')
                return user
            else:
                raise UnauthorisedAccessError(message='No permissions to view the user!')
        else:
            raise UnauthorisedAccessError(message='No permissions to view a user!')

    @login_required
    def resolve_user(self, info, **kwargs):
        if info.context.user.has_perm('account.can_view_custom_user'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                id = kwargs.get('id')
                if id is not None:
                    return get_user_model().objects.get(pk=id)
            else:
                raise UnauthorisedAccessError(message='No permissions to view the user!')
        else:
            raise UnauthorisedAccessError(message='No permissions to view a user!')

    @login_required
    def resolve_users(self, info):
        if info.context.user.has_perm('account.can_view_custom_user'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                return get_user_model().objects.all()
            else:
                raise UnauthorisedAccessError(message='No permissions to view the user!')
        else:
            raise UnauthorisedAccessError(message='No permissions to view a user!')

    @login_required
    def resolve_group(self, info, **kwargs):
        if info.context.user.has_perm('auth.can_update_group'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                name = kwargs.get('name')
                if name is not None:
                    return Group.objects.get(name=name)
            else:
                raise UnauthorisedAccessError(message='No permissions to view the group!')
        else:
            raise UnauthorisedAccessError(message='No permissions to view a group!')

    @login_required
    def resolve_groups(self, info, **kwargs):
        if info.context.user.has_perm('auth.can_update_group'):
            if info.context.user.groups.filter(name='Doctor').exists() or info.context.user.groups.filter(
                    name='Admin').exists():
                return Group.objects.all()
            else:
                raise UnauthorisedAccessError(message='No permissions to view the group!')
        else:
            raise UnauthorisedAccessError(message='No permissions to view a group!')


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()
    add_to_group = UpdateGroup.Field()
