from graphql import GraphQLError
from graphql_relay import from_global_id


def valid_id(global_id, type):
    try:
        print(type)
        print(from_global_id(global_id)[0])
        print(from_global_id(global_id)[1])
        print(type(type))
        print(type(from_global_id(global_id)[0]))
        print(type(from_global_id(global_id)[1]))


        if type(type) is type(from_global_id(global_id)[0]):
            return from_global_id(global_id)
    except:
        raise GraphQLError("Invalid ID 1")
    raise GraphQLError("InvalidID 2")


def has_group(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False
