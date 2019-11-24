import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from boards.models import *
from datetime import datetime
from graphql_jwt.decorators import login_required


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class BoardType(DjangoObjectType):
    class Meta:
        model = Board
        fields = ('name', 'description', 'creator')

    def resolve_creator(self, info):
        if info.context.user.has_perm('boards.view_creator_board'):
            return self.creator
        return None


class BoardInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()


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
                raise GraphQLError('Please provide complete information!')
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
                board_instance = Board.objects.get(pk=board_id)
                if board_instance:
                    if input.name:
                        board_instance.name = input.name
                    if input.description:
                        board_instance.description = input.description
                    board_instance.save()
                    return CreateBoard(board=board_instance)
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to change a board!')


class DeleteBoard(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        board_id = graphene.Int(required=True)

    board = graphene.Field(BoardType)

    @login_required
    def mutate(self, info, board_id):
        if info.context.user.has_perm('boards.can_delete_board'):
            try:
                board_instance = Board.objects.get(pk=board_id)
                if board_instance:
                    board_instance.delete()
                    return DeleteBoard(ok=True)
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a board!')


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = ('subject', 'last_updated', 'board', 'creator')

    def resolve_creator(self, info):
        if info.context.user.has_perm('boards.view_creator_topic'):
            return self.creator
        return None


class TopicInput(graphene.InputObjectType):
    id = graphene.ID()
    subject = graphene.String()
    last_updated = graphene.DateTime()
    board = graphene.Int()


class CreateTopic(graphene.Mutation):
    class Arguments:
        input = TopicInput(required=True)

    topic = graphene.Field(TopicType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('boards.can_add_topic'):
            if input.subject is not None and input.board is not None:
                try:
                    get_board = Board.objects.get(pk=input.board)
                    if get_board:
                        topic_instance = Topic(subject=input.subject, last_updated=datetime.now(), board=get_board, creator=info.context.user)
                        topic_instance.save()
                        return CreateTopic(topic=topic_instance)
                except Board.DoesNotExist:
                    raise GraphQLError('Board does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
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
                topic_instance = Topic.objects.get(pk=topic_id)
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')

            if topic_instance:
                if input.subject:
                    topic_instance.subject = input.subject
                topic_instance.last_updated = datetime.now()
                try:
                    topic_instance.board = Board.objects.get(pk=input.board)
                except Board.DoesNotExist:
                    raise GraphQLError('Board does not exist!')
                topic_instance.save()
                return CreateTopic(topic=topic_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to update a topic!')


class DeleteTopic(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        topic_id = graphene.Int(required=True)

    topic = graphene.Field(TopicType)

    @login_required
    def mutate(self, info, topic_id):
        if info.context.user.has_perm('boards.can_delete_topic'):
            try:
                topic_instance = Topic.objects.get(pk=topic_id)
                if topic_instance:
                    topic_instance.delete()
                    return DeleteTopic(ok=True)
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a topic!')


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('message', 'topics', 'created_at', 'created_by', 'updated_at', 'updated_by')

    def resolve_created_by(self, info):
        if info.context.user.has_perm('boards.view_created_by'):
            return self.created_by
        return None

    def resolve_updated_by(self, info):
        if info.context.user.has_perm('boards.view_updated_by'):
            return self.updated_by
        return None


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    message = graphene.String()
    topic = graphene.Int()


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('boards.can_add_post'):
            if input.message is not None and input.topic is not None:
                try:
                    get_topic = Topic.objects.get(pk=input.topic)
                    if get_topic:
                        post_instance = Post(message=input.message, topic=get_topic, created_by=info.context.user,
                                             updated_by=info.context.user, created_at=datetime.now(),
                                             updated_at=datetime.now())
                        post_instance.save()
                        return CreatePost(post=post_instance)
                except Topic.DoesNotExist:
                    raise GraphQLError('Topic does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
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
                post_instance = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:

                raise GraphQLError('Post does not exist!')
            if post_instance:
                if input.message:
                    post_instance.message = input.message
                try:
                    post_instance.topic = Topic.objects.get(pk=input.topic)
                except Topic.DoesNotExist:
                    raise GraphQLError('Topic does not exist!')
                post_instance.updated_by = info.context.user
                post_instance.updated_at = datetime.now()
                post_instance.save()
                return CreatePost(post=post_instance)


class DeletePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int(required=True)

    post = graphene.Field(TopicType)

    @login_required
    def mutate(self, info, post_id):
        if info.context.user.has_perm('boards.can_delete_post'):
            try:
                post_instance = Post.objects.get(pk=post_id)
                if post_instance:
                    post_instance.delete()
                    return DeletePost(ok=True)
            except Post.DoesNotExist:
                raise GraphQLError('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a post!')


class Query(graphene.ObjectType):
    get_board = graphene.Field(BoardType, id=graphene.Int())
    get_topic = graphene.Field(TopicType, id=graphene.Int())
    get_post = graphene.Field(PostType, id=graphene.Int())

    get_all_boards = graphene.List(BoardType)
    get_all_topics = graphene.List(TopicType)
    get_all_posts = graphene.List(PostType)

    @login_required
    def resolve_get_board(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_board'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Board.objects.get(pk=id)
                except Board.DoesNotExist:
                    raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the boards!')

    @login_required
    def resolve_get_topic(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_topic'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Topic.objects.get(pk=id)
                except Topic.DoesNotExist:
                    raise GraphQLError('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the topics!')

    @login_required
    def resolve_get_post(self, info, **kwargs):
        if info.context.user.has_perm('boards.can_view_post'):
            id = kwargs.get('id')
            if id is not None:
                try:
                    return Post.objects.get(pk=id)
                except Post.DoesNotExist:
                    raise GraphQLError('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the posts!')

    @login_required
    def resolve_all_boards(self, info):
        if info.context.user.has_perm('boards.can_view_board'):
            try:
                return Board.objects.all()
            except Board.DoesNotExist:
                raise GraphQLError('Board does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the boards!')

    @login_required
    def resolve_get_all_topics(self, info):
        if info.context.user.has_perm('boards.can_view_topic'):
            try:
                return Topic.objects.all()
            except Topic.DoesNotExist:
                raise GraphQLError('Topic does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the topics!')

    @login_required
    def resolve_get_all_posts(self, info):
        if info.context.user.has_perm('boards.can_view_post'):
            try:
                return Post.objects.all()
            except Post.DoesNotExist:
                raise GraphQLError('Post does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to see the posts!')


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
