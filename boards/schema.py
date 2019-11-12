import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from boards.models import Board, Topic, Post
from graphql import GraphQLError
from django.db.models import Q
from datetime import datetime
from graphql_jwt.decorators import staff_member_required
from django.contrib.auth import get_user_model

class BoardType(DjangoObjectType):
    class Meta:
        model = Board


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class BoardNode(DjangoObjectType):
    class Meta:
        model = Board
        filter_fields = ['name', 'description']
        interfaces = (relay.Node, )


class TopicNode(DjangoObjectType):
    class Meta:
        model = Topic
        filter_fields = ['subject', 'last_updated', 'board', 'starter']
        interfaces = (relay.Node, )


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ['message', 'topic', 'created_at', 'updated_at', 'created_by', 'updated_by']
        interfaces = (relay.Node, )


class BoardCreation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    board = graphene.Field(BoardType)

    @staff_member_required
    def mutate(self, info, name, description):
        board = Board(
            name=name,
            description=description,
        )
        board.save()

        return BoardCreation(
            id=board.id,
            name=name,
            description=description,
        )


class BoardMutation(graphene.Mutation):
    class Arguments:
        board_id = graphene.Int()
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    board = graphene.Field(BoardType)

    @staff_member_required
    def mutate(self, info, board_id, name, description):
        board = Board.objects.get(board_id)
        board.name = name
        board.description = description
        board.save()

"""
class TopicCreation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        subject = graphene.String(required=True)
        starter = get_user_model()

    topic = graphene.Field(TopicType)

    @staff_member_required
    def mutate(self, info, board_id, subject, starter):
        board = Board.objects.get(board_id)
        topic = Topic(
            subject=subject,
            last_updated=datetime.now(),
            board=board,
            starter=info.context.user,
        )
        topic.save()

        return TopicCreation(
            id=board.id,
            subject=subject,
            last_updated=datetime.now(),
            board=board,
            starter=info.context.user,
        )


class TopicMutation(graphene.Mutation):
    class Arguments:
        topic_id = graphene.Int()
        board_id = graphene.Int()
        subject = graphene.String(required=True)

    topic = graphene.Field(TopicType)

    @staff_member_required
    def mutate(self, info, board_id, topic_id, subject, last_updated):
        topic = Topic.objects.get(topic_id)
        topic.subject = subject
        topic.last_updated = datetime.now()
        topic.save()


class PostCreation(graphene.Mutation):
    id = graphene.ID()
    message = graphene.String(required=True)
    topic = graphene.String(required=True)
    created_by = graphene.Field(get_user_model())
    updated_by = graphene.Field(get_user_model())

    class Arguments:
        id = graphene.ID()
        message = graphene.String(required=True)
        topic = graphene.String(required=True)
        created_by = graphene.Field(get_user_model())
        updated_by = graphene.Field(get_user_model())

    def mutate(self, info, message, topic, created_by, updated_by):
        post = Post(
            message=message,
            topic=topic,
            created_by=created_by,
            updated_by=updated_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        post.save()

        return PostCreation(
            id=post.id,
            message=message,
            topic=topic,
            created_by=created_by,
            updated_by=updated_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


class PostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        message = graphene.String(required=True)
        topic = graphene.String(required=True)
        updated_by = graphene.Field(get_user_model())

    post = graphene.Field(PostType)

    def mutate(self, info, message, topic, updated_by):
        post = Board.objects.get(pk=id)
        post.message = message
        post.topic = topic
        post.updated_by = updated_by
        post.updated_at = datetime.now()
        post.save()
"""

class Query(graphene.ObjectType):
    board = relay.Node.Field(BoardNode)
    topic = relay.Node.Field(TopicNode)
    post = relay.Node.Field(PostNode)

    all_boards = DjangoFilterConnectionField(BoardNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_posts = DjangoFilterConnectionField(PostNode)


class Mutation(graphene.ObjectType):
    create_board = BoardCreation.Field()
    mutate_board = BoardMutation.Field()

"""
    create_topic = TopicCreation.Field()
    mutate_topic = TopicMutation.Field()

    create_post = PostCreation.Field()
    mutate_post = PostMutation.Field()
"""
