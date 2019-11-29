import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_relay import from_global_id
from graphene_django.filter import DjangoFilterConnectionField
from survey.models import *
from datetime import datetime
from graphql_jwt.decorators import login_required


def hasGroup(groups, info):
    for role in groups:
        if info.context.user.groups.filter(name=role).exists():
            return True
    return False


def checkIfTextAnswered(question, user):
    if TextAnswer.objects.filter(question=question, created_by=user):
        return True
    else:
        return False


def checkIfChoiceAnswered(question, user):
    if ChoiceAnswer.objects.filter(question=question, created_by=user):
        return True
    else:
        return False


def checkIfNumberAnswered(question, user):
    if NumberAnswer.objects.filter(question=question, created_by=user):
        return True
    else:
        return False


class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class SurveyFilter(django_filters.FilterSet):
    class Meta:
        model = Survey
        fields = ['survey_name', 'description', 'created_on', 'created_by', 'updated_on', 'updated_by', 'pub_date']


class SurveyType(DjangoObjectType):
    class Meta:
        model = Survey
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_survey_name(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.survey_name
        return None

    @login_required
    def resolve_description(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.description
        return None

    @login_required
    def resolve_created_on(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_on
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_by
        return None

    @login_required
    def resolve_updated_on(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_on
        return None

    @login_required
    def resolve_updated_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_by
        return None

    @login_required
    def resolve_pub_date(self, info):
        if hasGroup(["Admin", "Doctor"], info):
            return self.pub_date
        return None


class CreateSurvey(graphene.relay.ClientIDMutation):
    survey = graphene.Field(SurveyType)

    class Input:
        survey_name = graphene.String(required=True)
        description = graphene.String(required=True)
        pub_date = graphene.DateTime()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            survey_instance = Survey(survey_name=input.get('survey_name'), description=input.get('description'),
                                     created_on=datetime.now(), created_by=info.context.user,
                                     updated_on=datetime.now(), updated_by=info.context.user,
                                     pub_date=datetime.now() if input.get('pub_date') is None else input.get('pub_date'))
            survey_instance.save()
            return CreateSurvey(survey=survey_instance)
        else:
            raise UnauthorisedAccessError(message='No permissions to create a survey!')


class UpdateSurvey(graphene.relay.ClientIDMutation):
    survey = graphene.Field(SurveyType)

    class Input:
        id = graphene.ID(required=True)
        survey_name = graphene.String()
        description = graphene.String()
        pub_date = graphene.DateTime()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                survey_instance = Survey.objects.get(pk=from_global_id(input.get('id'))[1])
                if survey_instance:
                    if input.get('survey_name'):
                        survey_instance.survey_name = input.get('survey_name')
                    if input.get('description'):
                        survey_instance.description = input.get('description')
                    if input.get('pub_date'):
                        survey_instance.pub_date = input.get('pub_date')
                    survey_instance.updated_by = info.context.user
                    survey_instance.updated_on = datetime.now()
                    survey_instance.save()
                    return UpdateSurvey(survey=survey_instance)
            except Survey.DoesNotExist:
                raise GraphQLError('Survey does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a survey!')


class DeleteSurvey(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    survey = graphene.Field(SurveyType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                survey_instance = Survey.objects.get(pk=from_global_id(input.get('id'))[1])
                if survey_instance:
                    survey_instance.delete()
                    return DeleteSurvey(ok=True)
            except Survey.DoesNotExist:
                raise GraphQLError('Survey does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a survey!')


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['question_text', 'created_on', 'created_by', 'updated_on', 'updated_by', 'question_type', 'survey']


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_question_text(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.question_text
        return None

    @login_required
    def resolve_created_on(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_on
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.created_by
        return None

    @login_required
    def resolve_updated_on(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_on
        return None

    @login_required
    def resolve_updated_by(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.updated_by
        return None

    @login_required
    def resolve_question_type(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.question_type
        return None

    @login_required
    def resolve_survey(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.survey
        return None


class CreateQuestion(graphene.relay.ClientIDMutation):
    question = graphene.Field(QuestionType)

    class Input:
        question_text = graphene.String(required=True)
        question_type = graphene.String(required=True)
        survey = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                get_survey = Survey.objects.get(pk=from_global_id(input.get('survey'))[1])
                question_instance = Question(question_text=input.get('question_text'), created_on=datetime.now(),
                                             created_by=info.context.user, updated_on=datetime.now(),
                                             updated_by=info.context.user, question_type=input.get('question_type'),
                                             survey=get_survey)
                question_instance.save()
                return CreateQuestion(question=question_instance)
            except Question.DoesNotExist:
                raise GraphQLError('Survey does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a question!')


class UpdateQuestion(graphene.relay.ClientIDMutation):
    question = graphene.Field(QuestionType)

    class Input:
        id = graphene.ID(required=True)
        question_text = graphene.String()
        question_type = graphene.String()
        survey = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                question_instance = Question.objects.get(pk=from_global_id(input.get('id'))[1])
                if question_instance:
                    if input.get('question_text'):
                        question_instance.question_text = input.get('question_text')
                    if input.get('survey'):
                        try:
                            get_survey = Survey.objects.get(pk=from_global_id(input.get('survey'))[1])
                            question_instance.survey = get_survey
                        except Survey.DoesNotExist:
                            raise GraphQLError('Survey does not exist!')
                    question_instance.updated_by = info.context.user
                    question_instance.updated_on = datetime.now()
                    question_instance.save()
                    return UpdateQuestion(question=question_instance)
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a question!')


class DeleteQuestion(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    question = graphene.Field(QuestionType)

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                question_instance = Question.objects.get(pk=from_global_id(input.get('id'))[1])
                if question_instance:
                    question_instance.delete()
                    return DeleteQuestion(ok=True)
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a question!')


class ChoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Choice
        fields = ['choice_text', 'question']


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.id
        return -1

    @login_required
    def resolve_choice_text(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.choice_text
        return None

    @login_required
    def resolve_question(self, info):
        if hasGroup(["Admin", "Doctor", "Patient"], info):
            return self.question
        return None


class CreateChoice(graphene.relay.ClientIDMutation):
    choice = graphene.Field(ChoiceType)

    class Input:
        choice_text = graphene.String(required=True)
        question = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                if get_question.question_type == Question.CHOICE:
                    choice_instance = Choice(choice_text=input.get('choice_text'), question=get_question)
                    choice_instance.save()
                    return CreateChoice(choice=choice_instance)
                else:
                    raise GraphQLError('Wrong question type!')
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a choice!')


class UpdateChoice(graphene.relay.ClientIDMutation):
    choice = graphene.Field(ChoiceType)

    class Input:
        id = graphene.ID(required=True)
        choice_text = graphene.String()
        question = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                choice_instance = Choice.objects.get(pk=from_global_id(input.get('id'))[1])
                if choice_instance:
                    if input.get('choice_text'):
                        choice_instance.choice_text = input.get('choice_text')
                    if input.get('question'):
                        try:
                            get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                            choice_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    choice_instance.save()
                    return UpdateChoice(choice=choice_instance)
            except Choice.DoesNotExist:
                raise GraphQLError('Choice does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a choice!')


class DeleteChoice(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    choice = graphene.Field(ChoiceType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Doctor"], info):
            try:
                choice_instance = Choice.objects.get(pk=from_global_id(input.get('id'))[1])
                if choice_instance:
                    choice_instance.delete()
                    return DeleteChoice(ok=True)
            except Choice.DoesNotExist:
                raise GraphQLError('Choice does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a choice!')


class TextAnswerFilter(django_filters.FilterSet):
    class Meta:
        model = TextAnswer
        fields = ['text_answer', 'created_on', 'created_by', 'updated_on', 'question']


class TextAnswerType(DjangoObjectType):
    class Meta:
        model = TextAnswer
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.id
        return -1

    @login_required
    def resolve_created_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_on
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_by
        return None

    @login_required
    def resolve_updated_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.updated_on
        return None

    @login_required
    def resolve_text_answer(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.text_answer
        return None

    @login_required
    def resolve_question(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.question
        return None


class CreateTextAnswer(graphene.relay.ClientIDMutation):
    text_answer = graphene.Field(TextAnswerType)

    class Input:
        text_answer = graphene.String(required=True)
        question = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                if checkIfTextAnswered(get_question, info.context.user):
                    if get_question.question_type == Question.TEXT:
                        text_answer_instance = TextAnswer(text_answer=input.get('text_answer'), question=get_question)
                        text_answer_instance.save()
                        return CreateTextAnswer(text_answer=text_answer_instance)
                    else:
                        raise GraphQLError('Wrong question type!')
                else:
                    raise GraphQLError('Question already answered!')
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a text answer!')


class UpdateTextAnswer(graphene.relay.ClientIDMutation):
    text_answer = graphene.Field(TextAnswerType)

    class Input:
        id = graphene.ID(required=True)
        text_answer = graphene.String()
        question = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if text_answer_instance:
                    if input.get('text_answer'):
                        text_answer_instance.text_answer = input.get('text_answer')
                    if input.get('question'):
                        try:
                            get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                            text_answer_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    text_answer_instance.save()
                    return UpdateTextAnswer(text_answer=text_answer_instance)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a text answer!')


class DeleteTextAnswer(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    text_answer = graphene.Field(TextAnswerType)

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if text_answer_instance:
                    text_answer_instance.delete()
                    return DeleteTextAnswer(ok=True)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a text answer!')


class NumberAnswerFilter(django_filters.FilterSet):
    class Meta:
        model = NumberAnswer
        fields = ['number_answer', 'created_on', 'created_by', 'updated_on', 'question']


class NumberAnswerType(DjangoObjectType):
    class Meta:
        model = NumberAnswer
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.id
        return -1

    @login_required
    def resolve_created_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_on
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_by
        return None

    @login_required
    def resolve_updated_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.updated_on
        return None

    @login_required
    def resolve_number_answer(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.number_answer
        return None

    @login_required
    def resolve_question(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.question
        return None


class CreateNumberAnswer(graphene.relay.ClientIDMutation):
    number_answer = graphene.Field(NumberAnswerType)

    class Input:
        number_answer = graphene.String(required=True)
        question = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                if checkIfNumberAnswered(get_question, info.context.user):
                    if get_question.question_type == Question.NUMBER:
                        number_answer_instance = NumberAnswer(number_answer=input.get('number_answer'), question=get_question)
                        number_answer_instance.save()
                        return CreateNumberAnswer(number_answer=number_answer_instance)
                    else:
                        raise GraphQLError('Wrong question type!')
                else:
                    raise GraphQLError('Question already answered!')
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a number answer!')


class UpdateNumberAnswer(graphene.relay.ClientIDMutation):
    number_answer = graphene.Field(NumberAnswerType)

    class Input:
        id = graphene.ID(required=True)
        number_answer = graphene.String()
        question = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                number_answer_instance = NumberAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if number_answer_instance:
                    if input.get('number_answer'):
                        number_answer_instance.number_answer = input.get('number_answer')
                    if input.get('question'):
                        try:
                            get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                            number_answer_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    number_answer_instance.save()
                    return UpdateNumberAnswer(number_answer=number_answer_instance)
            except NumberAnswer.DoesNotExist:
                raise GraphQLError('Number answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a number answer!')


class DeleteNumberAnswer(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    number_answer = graphene.Field(NumberAnswerType)

    class Inputs:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                number_answer_instance = NumberAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if number_answer_instance:
                    number_answer_instance.delete()
                    return DeleteNumberAnswer(ok=True)
            except NumberAnswer.DoesNotExist:
                raise GraphQLError('Number answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a number answer!')


class ChoiceAnswerFilter(django_filters.FilterSet):
    class Meta:
        model = ChoiceAnswer
        fields = ['choice_answer', 'created_on', 'created_by', 'updated_on', 'question']


class ChoiceAnswerType(DjangoObjectType):
    class Meta:
        model = ChoiceAnswer
        interfaces = (graphene.relay.Node,)

    @login_required
    def resolve_id(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.id
        return -1

    @login_required
    def resolve_created_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_on
        return None

    @login_required
    def resolve_created_by(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.created_by
        return None

    @login_required
    def resolve_updated_on(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.updated_on
        return None

    @login_required
    def resolve_choice_answer(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.choice_answer
        return None

    @login_required
    def resolve_question(self, info):
        if hasGroup(["Admin", "Doctor"], info) or self.created_by == info.context.user:
            return self.question
        return None


class CreateChoiceAnswer(graphene.relay.ClientIDMutation):
    choice_answer = graphene.Field(ChoiceAnswerType)

    class Input:
        choice_answer = graphene.ID(required=True)
        question = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                if checkIfChoiceAnswered(get_question, info.context.user):
                    if get_question.question_type == Question.CHOICE:
                        try:
                            get_choice = Choice.objects.get(pk=from_global_id(input.get('choice_answer'))[1])
                            choice_answer_instance = ChoiceAnswer(choice_answer=get_choice,
                                                                  question=get_question)
                            choice_answer_instance.save()
                            return CreateChoiceAnswer(choice_answer=choice_answer_instance)
                        except Choice.DoesNotExist:
                            raise GraphQLError('Choice does not exist!')
                    else:
                        raise GraphQLError('Wrong question type!')
                else:
                    raise GraphQLError('Question already answered!')
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a choice answer!')


class UpdateChoiceAnswer(graphene.relay.ClientIDMutation):
    choice_answer = graphene.Field(ChoiceAnswerType)

    class Input:
        id = graphene.ID(required=True)
        choice_answer = graphene.ID()
        question = graphene.ID()

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                choice_answer_instance = ChoiceAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if choice_answer_instance:
                    if input.get('choice_answer'):
                        try:
                            get_choice = Choice.objects.get(pk=from_global_id(input.get('choice_answer'))[1])
                            choice_answer_instance.choice_answer = get_choice
                        except Choice.DoesNotExist:
                            raise GraphQLError('Choice does not exist!')
                    if input.get('question'):
                        try:
                            get_question = Question.objects.get(pk=from_global_id(input.get('question'))[1])
                            choice_answer_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    choice_answer_instance.save()
                    return UpdateChoiceAnswer(choice_answer=choice_answer_instance)
            except ChoiceAnswer.DoesNotExist:
                raise GraphQLError('Choice answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a choice answer!')


class DeleteChoiceAnswer(graphene.relay.ClientIDMutation):
    ok = graphene.Boolean()
    choice_answer = graphene.Field(ChoiceAnswerType)

    class Input:
        id = graphene.ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, **input):
        if hasGroup(["Admin", "Patient"], info):
            try:
                choice_answer_instance = ChoiceAnswer.objects.get(pk=from_global_id(input.get('id'))[1])
                if choice_answer_instance:
                    choice_answer_instance.delete()
                    return DeleteChoiceAnswer(ok=True)
            except ChoiceAnswer.DoesNotExist:
                raise GraphQLError('Choice answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a choice answer!')


class Query(graphene.ObjectType):
    get_survey = graphene.relay.Node.Field(SurveyType)
    get_question = graphene.relay.Node.Field(QuestionType)
    get_choice = graphene.relay.Node.Field(ChoiceType)
    get_text_answer = graphene.relay.Node.Field(TextAnswerType)
    get_choice_answer = graphene.relay.Node.Field(ChoiceAnswerType)
    get_number_answer = graphene.relay.Node.Field(NumberAnswerType)

    get_surveys = DjangoFilterConnectionField(SurveyType, filterset_class=SurveyFilter)
    get_questions = DjangoFilterConnectionField(QuestionType, filterset_class=QuestionFilter)
    get_choices = DjangoFilterConnectionField(ChoiceType, filterset_class=ChoiceFilter)
    get_text_answers = DjangoFilterConnectionField(TextAnswerType, filterset_class=TextAnswerFilter)
    get_choice_answers = DjangoFilterConnectionField(ChoiceAnswerType, filterset_class=ChoiceAnswerFilter)
    get_number_answers = DjangoFilterConnectionField(NumberAnswerType, filterset_class=NumberAnswerFilter)


class Mutation(graphene.ObjectType):
    create_survey = CreateSurvey.Field()
    create_question = CreateQuestion.Field()
    create_choice = CreateChoice.Field()
    create_text_answer = CreateTextAnswer.Field()
    create_choice_answer = CreateChoiceAnswer.Field()
    create_number_answer = CreateNumberAnswer.Field()

    update_survey = UpdateSurvey.Field()
    update_question = UpdateQuestion.Field()
    update_choice = UpdateChoice.Field()
    update_text_answer = UpdateTextAnswer.Field()
    update_choice_answer = UpdateChoiceAnswer.Field()
    update_number_answer = UpdateNumberAnswer.Field()

    delete_survey = DeleteSurvey.Field()
    delete_question = DeleteQuestion.Field()
    delete_choice = DeleteChoice.Field()
    delete_text_answer = DeleteTextAnswer.Field()
    delete_choice_answer = DeleteChoiceAnswer.Field()
    delete_number_answer = DeleteNumberAnswer.Field()
