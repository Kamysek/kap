import graphene
import graphql_jwt
import account.schema
import appointments.schema
import survey.schema


class Query(
    account.schema.Query,
	appointments.schema.Query,
    survey.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    account.schema.Mutation,
	appointments.schema.Mutation,
    survey.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
