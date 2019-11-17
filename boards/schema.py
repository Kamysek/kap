import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from boards.models import Board, Topic, Post
from datetime import datetime
from graphql_jwt.decorators import staff_member_required
from graphql_jwt.decorators import login_required
from graphql_jwt.decorators import user_passes_test


class BoardType(DjangoObjectType):
    class Meta:
        model = Board


class BoardNode(DjangoObjectType):
    class Meta:
        model = Board
        filter_fields = ['name', 'description', 'creator']
        interfaces = (relay.Node, )


class BoardInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class CreateBoard(graphene.Mutation):
    class Arguments:
        input = BoardInput(required=True)

    board = graphene.Field(BoardType)

    @login_required
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, input=None):
        board_instance = Board(name=input.name, description=input.description, creator=info.context.user)
        board_instance.save()
        return CreateBoard(board=board_instance)


class UpdateBoard(graphene.Mutation):
    class Arguments:
        board_id = graphene.Int(required=True)
        input = BoardInput(required=True)

    board = graphene.Field(BoardType)

    @login_required
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, board_id, input=None):
        board_instance = Board.objects.get(id=board_id)
        if board_instance:
            board_instance.name = input.name
            board_instance.description = input.description
            board_instance.save()
            return CreateBoard(board=board_instance)


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class TopicNode(DjangoObjectType):
    class Meta:
        model = Topic
        filter_fields = ['subject', 'last_updated', 'board', 'creator']
        interfaces = (relay.Node, )


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
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, input=None):
        topic_instance = Topic(subject=input.subject,
                               last_updated=datetime.now(),
                               board=Board.objects.get(id=input.board),
                               creator=info.context.user)
        topic_instance.save()
        return CreateTopic(topic=topic_instance)


class UpdateTopic(graphene.Mutation):
    class Arguments:
        topic_id = graphene.Int(required=True)
        input = TopicInput(required=True)

    topic = graphene.Field(TopicType)

    @login_required
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, topic_id, input=None):
        topic_instance = Topic.objects.get(id=topic_id)

        if topic_instance:
            topic_instance.subject = input.subject
            topic_instance.last_updated = datetime.now()
            topic_instance.board = Board.objects.get(id=input.board)
            topic_instance.save()
            return CreateTopic(topic=topic_instance)


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ['message', 'topic', 'created_at', 'updated_at', 'created_by', 'updated_by']
        interfaces = (relay.Node, )


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    message = graphene.String()
    topic = graphene.Int()


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @login_required
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, input=None):
        post_instance = Post(message=input.message,
                             topic=Topic.objects.get(id=input.topic),
                             created_by=info.context.user,
                             updated_by=info.context.user,
                             created_at=datetime.now(),
                             updated_at=datetime.now())
        post_instance.save()
        return CreatePost(post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @login_required
    @user_passes_test(
        lambda user: user.groups.filter(name='Doctor').exists() or user.groups.filter(name='Admin').exists())
    def mutate(self, info, post_id, input=None):
        post_instance = Post.objects.get(id=post_id)
        if post_instance:
            post_instance.message = input.message
            post_instance.topic = Topic.objects.get(id=input.topic)
            post_instance.updated_by = info.context.user
            post_instance.updated_at = datetime.now()
            post_instance.save()
            return CreatePost(post=post_instance)


class Query(graphene.ObjectType):

    board = relay.Node.Field(BoardNode)
    topic = relay.Node.Field(TopicNode)
    post = relay.Node.Field(PostNode)

    all_boards = DjangoFilterConnectionField(BoardNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_posts = DjangoFilterConnectionField(PostNode)


class Mutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    create_topic = CreateTopic.Field()
    create_post = CreatePost.Field()

    update_board = UpdateBoard.Field()
    update_topic = UpdateTopic.Field()
    update_post = UpdatePost.Field()