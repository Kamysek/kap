from graphql import GraphQLError
from graphql_relay import from_global_id


def validId(global_id):
    try:
        return from_global_id(global_id)
    except:
        raise GraphQLError("Invalid ID")