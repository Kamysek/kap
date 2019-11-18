import graphene
import graphql_jwt
import boards.schema
import account.schema
import appointments.schema


class Query(
    account.schema.Query,
    boards.schema.Query,
	appointments.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    account.schema.Mutation,
    boards.schema.Mutation,
	appointments.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
