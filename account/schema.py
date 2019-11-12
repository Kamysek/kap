import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import staff_member_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @staff_member_required
    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @staff_member_required
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @staff_member_required
    def resolve_me(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
