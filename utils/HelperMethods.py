from graphql import GraphQLError
from graphql_relay import from_global_id


def valid_id(global_id, type):
    try:
        print(str(type))
        print(str(from_global_id(global_id)[0]))
        if str(type) == str(from_global_id(global_id)[0]):
            return from_global_id(global_id)
    except:
        raise GraphQLError("Invalid ID")
    raise GraphQLError("InvalidID")


def has_group(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)