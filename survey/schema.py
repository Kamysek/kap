import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from survey.models import *
from datetime import datetime
from graphql_jwt.decorators import login_required


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class SurveyType(DjangoObjectType):
    class Meta:
        model = Survey


class SurveyInput(graphene.InputObjectType):
    id = graphene.ID()
    survey_name = graphene.String(required=True)
    description = graphene.String(required=True)
    pub_date = graphene.DateTime()


