import graphene
from django.contrib.auth.models import Permission
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from boards.models import Board, Topic, Post
from datetime import datetime
from graphql_jwt.decorators import login_required
from graphql_jwt.decorators import user_passes_test


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class BoardType(DjangoObjectType):
    class Meta:
        model = Board


class BoardInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class CreateBoard(graphene.Mutation):
    class Arguments:
        input = BoardInput(required=True)

    board = graphene.Field(BoardType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('boards.can_add_board'):
            if input.name is not None and input.description is not None and info.context.user is not None:
                board_instance = Board(name=input.name, description=input.description, creator=info.context.user)
                board_instance.save()
                return CreateBoard(board=board_instance)
            else:
                raise Exception('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a board!')


class UpdateBoard(graphene.Mutation):
    class Arguments:
        board_id = graphene.Int(required=True)
        input = BoardInput(required=True)

    board = graphene.Field(BoardType)

    @login_required
    def mutate(self, info, board_id, input=None):
        if info.context.user.has_perm('boards.can_change_board'):
            try:
                board_instance = Board.objects.get(id=board_id)
                if board_instance:
                    if input.name:
                        board_instance.name = input.name
                    if input.description:
                        board_instance.description = input.description
                    board_instance.save()
                    return CreateBoard(board=board_instance)
            except Board.DoesNotExist:
                raise Exception('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a board!')


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class TopicInput(graphene.InputObjectType):
    id = graphene.ID()
    subject = graphene.String(required=True)
    last_updated = graphene.DateTime()
    board = graphene.Int(required=True)


class CreateTopic(graphene.Mutation):
    class Arguments:
        input = TopicInput(required=True)

    topic = graphene.Field(TopicType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('boards.can_add_topic'):
            if input.subject is not None:
                try:
                    get_board = Board.objects.get(id=input.board)
                    if get_board:
                        topic_instance = Topic(subject=input.subject, last_updated=datetime.now(), board=get_board, creator=info.context.user)
                        topic_instance.save()
                        return CreateTopic(topic=topic_instance)
                except Board.DoesNotExist:
                    raise Exception('Board does not exist!')
            else:
                raise Exception('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a topic!')


class UpdateTopic(graphene.Mutation):
    class Arguments:
        topic_id = graphene.Int(required=True)
        input = TopicInput(required=True)

    topic = graphene.Field(TopicType)

    @login_required
    def mutate(self, info, topic_id, input=None):
        if info.context.user.has_perm('boards.can_change_topic'):
            try:
                topic_instance = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                raise Exception('Topic does not exist!')

            if topic_instance:
                if input.subject:
                    topic_instance.subject = input.subject
                topic_instance.last_updated = datetime.now()
                try:
                    topic_instance.board = Board.objects.get(id=input.board)
                except Board.DoesNotExist:
                    raise Exception('Board does not exist!')
                topic_instance.save()
                return CreateTopic(topic=topic_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to update a topic!')


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    message = graphene.String(required=True)
    topic = graphene.Int(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('boards.can_add_post'):
            if input.message is not None and input.topic is not None:
                try:
                    get_topic = Topic.objects.get(id=input.topic)
                    if get_topic:
                        post_instance = Post(message=input.message, topic=get_topic, created_by=info.context.user,
                                             updated_by=info.context.user, created_at=datetime.now(),
                                             updated_at=datetime.now())
                        post_instance.save()
                        return CreatePost(post=post_instance)
                except Topic.DoesNotExist:
                    raise Exception('Topic does not exist!')
            else:
                raise Exception('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a post!')


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id, input=None):

        if info.context.user.has_perm('boards.can_change_post'):
            try:
                post_instance = Post.objects.get(id=post_id)
            except Post.DoesNotExist:

                raise Exception('Post does not exist!')
            if post_instance:
                if input.message:
                    post_instance.message = input.message
                try:
                    post_instance.topic = Topic.objects.get(id=input.topic)
                except Topic.DoesNotExist:
                    raise Exception('Topic does not exist!')
                post_instance.updated_by = info.context.user
                post_instance.updated_at = datetime.now()
                post_instance.save()
                return CreatePost(post=post_instance)


class Query(graphene.ObjectType):
    board = graphene.Field(BoardType, id=graphene.Int())
    topic = graphene.Field(TopicType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())

    all_boards = graphene.List(BoardType)
    all_topics = graphene.List(TopicType)
    all_posts = graphene.List(PostType)

    def resolve_board(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_board'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Board.objects.get(id=id)
                except Board.DoesNotExist:
                    raise Exception('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the boards!')

    def resolve_topic(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_topic'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Topic.objects.get(id=id)
                except Topic.DoesNotExist:
                    raise Exception('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the topics!')

    def resolve_post(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_post'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Post.objects.get(id=id)
                except Post.DoesNotExist:
                    raise Exception('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the posts!')

    def resolve_all_boards(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_board'):
            try:
                return Board.objects.all()
            except Board.DoesNotExist:
                raise Exception('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the boards!')

    def resolve_all_topics(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_topic'):
            try:
                return Topic.objects.all()
            except Topic.DoesNotExist:
                raise Exception('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the topics!')

    def resolve_all_posts(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_post'):
            try:
                return Post.objects.all()
            except Post.DoesNotExist:
                raise Exception('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the posts!')


class Mutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    create_topic = CreateTopic.Field()
    create_post = CreatePost.Field()

    update_board = UpdateBoard.Field()
    update_topic = UpdateTopic.Field()
    update_post = UpdatePost.Field()
