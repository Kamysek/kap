import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay import from_global_id

from boards.models import *
from datetime import datetime
from graphql_jwt.decorators import login_required


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


def hasGroup(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


class BoardFilter(django_filters.FilterSet):
    class Meta:
        model = Board
        fields = ['name', 'description', 'creator']


class BoardType(DjangoObjectType):
    class Meta:
        model = Board
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_name(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.name
        return None

    @login_required
    def resolve_description(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.description
        return None

    @login_required
    def resolve_creator(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.creator
        return None


class CreateBoard(graphene.relay.ClientIDMutation):
    board = graphene.Field(BoardType)

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            board_instance = Board(name=input.get('name'), description=input.get('description'), creator=info.context.user)
            board_instance.save()
            return CreateBoard(board=board_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a board!')


class UpdateBoard(graphene.relay.ClientIDMutation):
    board = graphene.Field(BoardType)

    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                board_instance = Board.objects.get(pk=from_global_id(input.get('id'))[1])
                if board_instance:
                    if input.get('name'):
                        board_instance.name = input.get('name')
                    if input.get('description'):
                        board_instance.description = input.get('description')
                    board_instance.save()
                    return CreateBoard(board=board_instance)
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a board!')


class DeleteBoard(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    board = graphene.Field(BoardType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                board_instance = Board.objects.get(pk=from_global_id(input.get('id'))[1])
                if board_instance:
                    board_instance.delete()
                    return DeleteBoard(ok=True)
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a board!')


class TopicFilter(django_filters.FilterSet):
    class Meta:
        model = Topic
        fields = ['subject', 'last_updated', 'board', 'creator']


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_subject(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.subject
        return None

    @login_required
    def resolve_last_updated(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.last_updated
        return None

    @login_required
    def resolve_creator(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.creator
        return None


class CreateTopic(graphene.relay.ClientIDMutation):
    topic = graphene.Field(TopicType)

    class Input:
        subject = graphene.String(required=True)
        board = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                get_board = Board.objects.get(pk=from_global_id(input.get('board'))[1])
                if get_board:
                    topic_instance = Topic(subject=input.get('subject'), last_updated=datetime.now(), board=get_board, creator=info.context.user)
                    topic_instance.save()
                    return CreateTopic(topic=topic_instance)
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a topic!')


class UpdateTopic(graphene.relay.ClientIDMutation):
    topic = graphene.Field(TopicType)

    class Input:
        id = graphene.ID(required=True)
        subject = graphene.String()
        board = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                topic_instance = Topic.objects.get(pk=from_global_id(input.get('id'))[1])
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')

            if topic_instance:
                if input.get('subject'):
                    topic_instance.subject = input.get('subject')
                topic_instance.last_updated = datetime.now()
                try:
                    if input.get('board'):
                        topic_instance.board = Board.objects.get(pk=from_global_id(input.get('board'))[1])
                except Board.DoesNotExist:
                    raise GraphQLError('Board does not exist!')
                topic_instance.save()
                return CreateTopic(topic=topic_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to update a topic!')


class DeleteTopic(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    topic = graphene.Field(TopicType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                topic_instance = Topic.objects.get(pk=from_global_id(input.get('id'))[1])
                if topic_instance:
                    topic_instance.delete()
                    return DeleteTopic(ok=True)
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a topic!')


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['message', 'topic', 'created_at', 'created_by', 'updated_at']


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_message(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.message
        return None

    @login_required
    def resolve_topic(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.topic
        return None

    @login_required
    def resolve_created_at(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_at
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_by
        return None

    @login_required
    def resolve_updated_at(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_at
        return None

    @login_required
    def resolve_updated_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_by
        return None


class CreatePost(graphene.relay.ClientIDMutation):
    post = graphene.Field(PostType)

    class Input:
        message = graphene.String(required=True)
        topic = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                get_topic = Topic.objects.get(pk=from_global_id(input.get('topic'))[1])
                if get_topic:
                    post_instance = Post(message=input.get('message'), topic=get_topic, created_by=info.context.user,
                                         updated_by=info.context.user, created_at=datetime.now(),
                                         updated_at=datetime.now())
                    post_instance.save()
                    return CreatePost(post=post_instance)
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a post!')


class UpdatePost(graphene.relay.ClientIDMutation):
    post = graphene.Field(PostType)

    class Input:
        id = graphene.ID(required=True)
        message = graphene.String()
        topic = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                post_instance = Post.objects.get(pk=from_global_id(input.get('id'))[1])
            except Post.DoesNotExist:
                raise GraphQLError('Post does not exist!')
            if post_instance:
                if input.get('message'):
                    post_instance.message = input.get('message')
                try:
                    if input.get('topic'):
                        post_instance.topic = Topic.objects.get(pk=from_global_id(input.get('topic'))[1])
                except Topic.DoesNotExist:
                    raise GraphQLError('Topic does not exist!')
                post_instance.updated_by = info.context.user
                post_instance.updated_at = datetime.now()
                post_instance.save()
                return CreatePost(post=post_instance)


class DeletePost(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    post = graphene.Field(TopicType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                post_instance = Post.objects.get(pk=from_global_id(input.get('id'))[1])
                if post_instance:
                    post_instance.delete()
                    return DeletePost(ok=True)
            except Post.DoesNotExist:
                raise GraphQLError('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a post!')


class Query(graphene.ObjectType):
    get_board = graphene.relay.Node.Field(BoardType)
    get_topic = graphene.relay.Node.Field(TopicType)
    get_post = graphene.relay.Node.Field(PostType)

    get_boards = DjangoFilterConnectionField(BoardType, filterset_class=BoardFilter)
    get_topics = DjangoFilterConnectionField(TopicType, filterset_class=TopicFilter)
    get_posts = DjangoFilterConnectionField(PostType, filterset_class=PostFilter)


class Mutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    create_topic = CreateTopic.Field()
    create_post = CreatePost.Field()

    update_board = UpdateBoard.Field()
    update_topic = UpdateTopic.Field()
    update_post = UpdatePost.Field()

    delete_board = DeleteBoard.Field()
    delete_topic = DeleteTopic.Field()
    delete_post = DeletePost.Field()
