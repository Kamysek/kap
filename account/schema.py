import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from account.models import CustomUser
from graphql_jwt.decorators import staff_member_required


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

    #@ staff_member_required
    def mutate(self, info, input=None):
        user_instance = get_user_model()(
            username=input.username,
        )
        user_instance.set_password(input.password)
        user_instance.save()

        return CreateUser(user=user_instance)


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return get_user_model().objects.get(pk=id)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info, **kwargs):
        return info.context.user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
