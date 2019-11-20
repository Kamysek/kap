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
    survey_name = graphene.String()
    description = graphene.String()
    pub_date = graphene.DateTime()


class CreateSurvey(graphene.Mutation):
    class Arguments:
        input = SurveyInput(required=True)

    survey = graphene.Field(SurveyType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('survey.can_add_survey'):
            if input.survey_name is not None and input.description is not None and info.context.user is not None:
                if input.pub_date is None:
                    survey_instance = Survey(survey_name=input.survey_name, description=input.description,
                                             created_on=datetime.now(), created_by=info.context.user,
                                             updated_on=datetime.now(), updated_by=info.context.user,
                                             pub_date=datetime.now())
                else:
                    survey_instance = Survey(survey_name=input.survey_name, description=input.description,
                                             created_on=datetime.now(), created_by=info.context.user,
                                             updated_on=datetime.now(), updated_by=info.context.user,
                                             pub_date=input.pub_date)
                survey_instance.save()
                return CreateSurvey(survey=survey_instance)
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a survey!')


class UpdateSurvey(graphene.Mutation):
    class Arguments:
        survey_id = graphene.Int(required=True)
        input = SurveyInput(required=True)

    survey = graphene.Field(SurveyType)

    @login_required
    def mutate(self, info, survey_id, input=None):
        if info.context.user.has_perm('survey.can_change_survey'):
            try:
                survey_instance = Survey.objects.get(pk=survey_id)
                if survey_instance:
                    if input.survey_name:
                        survey_instance.survey_name = input.survey_name
                    if input.description:
                        survey_instance.description = input.description
                    if input.pub_date:
                        survey_instance.pub_date = input.pub_date
                    survey_instance.updated_by = info.context.user
                    survey_instance.updated_on = datetime.now()
                    survey_instance.save()
                    return UpdateSurvey(survey=survey_instance)
            except Survey.DoesNotExist:
                raise GraphQLError('Survey does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a survey!')


class DeleteSurvey(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        survey_id = graphene.Int(required=True)

    survey = graphene.Field(SurveyType)

    @login_required
    def mutate(self, info, survey_id):
        if info.context.user.has_perm('survey.can_delete_survey'):
            try:
                survey_instance = Survey.objects.get(pk=survey_id)
                if survey_instance:
                    survey_instance.delete()
                    return DeleteSurvey(ok=True)
            except Survey.DoesNotExist:
                raise GraphQLError('Survey does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a survey!')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class QuestionInput(graphene.InputObjectType):
    id = graphene.ID()
    question_text = graphene.String()
    question_type = graphene.String()
    survey = graphene.Int()


class CreateQuestion(graphene.Mutation):
    class Arguments:
        input = QuestionInput(required=True)

    question = graphene.Field(QuestionType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('survey.can_add_question'):
            if input.question_text is not None and input.question_type is not None and info.context.user is not None:
                try:
                    get_survey = Survey.objects.get(pk=input.survey)
                    question_instance = Question(question_text=input.question_text, created_on=datetime.now(),
                                                 created_by=info.context.user, updated_on=datetime.now(),
                                                 updated_by=info.context.user, question_type=input.question_type,
                                                 survey=get_survey)
                    question_instance.save()
                    return CreateQuestion(question=question_instance)
                except Question.DoesNotExist:
                    raise GraphQLError('Survey does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a question!')


class UpdateQuestion(graphene.Mutation):
    class Arguments:
        question_id = graphene.Int(required=True)
        input = QuestionInput(required=True)

    question = graphene.Field(QuestionType)

    @login_required
    def mutate(self, info, question_id, input=None):
        if info.context.user.has_perm('survey.can_change_question'):
            try:
                question_instance = Question.objects.get(pk=question_id)
                if question_instance:
                    if input.question_text:
                        question_instance.question_text = input.question_text
                    if input.survey:
                        try:
                            get_survey = Survey.objects.get(pk=input.survey)
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


class DeleteQuestion(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        question_id = graphene.Int(required=True)

    question = graphene.Field(QuestionType)

    @login_required
    def mutate(self, info, question_id):
        if info.context.user.has_perm('survey.can_delete_question'):
            try:
                question_instance = Question.objects.get(pk=question_id)
                if question_instance:
                    question_instance.delete()
                    return DeleteQuestion(ok=True)
            except Question.DoesNotExist:
                raise GraphQLError('Question does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a question!')


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice


class ChoiceInput(graphene.InputObjectType):
    id = graphene.ID()
    choice_text = graphene.String(required=True)
    question = graphene.Int(required=True)


class CreateChoice(graphene.Mutation):
    class Arguments:
        input = ChoiceInput(required=True)

    choice = graphene.Field(ChoiceType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('survey.can_add_choice'):
            if input.choice_text is not None and input.question is not None and info.context.user is not None:
                try:
                    get_question = Question.objects.get(pk=input.question)
                    if get_question.question_type == Question.CHOICE:
                        choice_instance = Choice(choice_text=input.choice_text, question=get_question)
                        choice_instance.save()
                        return CreateChoice(choice=choice_instance)
                    else:
                        raise GraphQLError('Wrong question type!')
                except Question.DoesNotExist:
                    raise GraphQLError('Question does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a choice!')


class UpdateChoice(graphene.Mutation):
    class Arguments:
        choice_id = graphene.Int(required=True)
        input = ChoiceInput(required=True)

    choice = graphene.Field(ChoiceType)

    @login_required
    def mutate(self, info, choice_id, input=None):
        if info.context.user.has_perm('survey.can_change_choice'):
            try:
                choice_instance = Choice.objects.get(pk=choice_id)
                if choice_instance:
                    if input.choice_text:
                        choice_instance.choice_text = input.choice_text
                    if input.question:
                        try:
                            get_question = Question.objects.get(pk=input.question)
                            choice_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    choice_instance.save()
                    return UpdateChoice(choice=choice_instance)
            except Choice.DoesNotExist:
                raise GraphQLError('Choice does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a choice!')


class DeleteChoice(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        choice_id = graphene.Int(required=True)

    choice = graphene.Field(ChoiceType)

    @login_required
    def mutate(self, info, choice_id):
        if info.context.user.has_perm('survey.can_delete_choice'):
            try:
                choice_instance = Choice.objects.get(pk=choice_id)
                if choice_instance:
                    choice_instance.delete()
                    return DeleteChoice(ok=True)
            except Choice.DoesNotExist:
                raise GraphQLError('Choice does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a choice!')


class TextAnswerType(DjangoObjectType):
    class Meta:
        model = TextAnswer


class TextAnswerInput(graphene.InputObjectType):
    id = graphene.ID()
    text_answer = graphene.String(required=True)
    question = graphene.Int(required=True)


class CreateTextAnswer(graphene.Mutation):
    class Arguments:
        input = TextAnswerInput(required=True)

    text_answer = graphene.Field(TextAnswerType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('survey.can_add_text_answer'):
            if input.text_answer is not None and input.question is not None and info.context.user is not None:
                try:
                    get_question = Question.objects.get(pk=input.question)
                    if get_question.question_type == Question.TEXT:
                        text_answer_instance = TextAnswer(text_answer=input.text_answer, question=get_question)
                        text_answer_instance.save()
                        return CreateTextAnswer(text_answer=text_answer_instance)
                    else:
                        raise GraphQLError('Wrong question type!')
                except Question.DoesNotExist:
                    raise GraphQLError('Question does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a text answer!')


class UpdateTextAnswer(graphene.Mutation):
    class Arguments:
        text_answer_id = graphene.Int(required=True)
        input = TextAnswerInput(required=True)

    text_answer = graphene.Field(TextAnswerType)

    @login_required
    def mutate(self, info, text_answer_id, input=None):
        if info.context.user.has_perm('survey.can_change_text_answer'):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=text_answer_id)
                if text_answer_instance:
                    if input.text_answer:
                        text_answer_instance.text_answer = input.text_answer
                    if input.question:
                        try:
                            get_question = Question.objects.get(pk=input.question)
                            text_answer_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    text_answer_instance.save()
                    return UpdateTextAnswer(text_answer=text_answer_instance)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a text answer!')


class DeleteTextAnswer(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        text_answer_id = graphene.Int(required=True)

    text_answer = graphene.Field(TextAnswerType)

    @login_required
    def mutate(self, info, text_answer_id):
        if info.context.user.has_perm('survey.can_delete_text_answer'):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=text_answer_id)
                if text_answer_instance:
                    text_answer_instance.delete()
                    return DeleteTextAnswer(ok=True)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a text answer!')


class NumberAnswerType(DjangoObjectType):
    class Meta:
        model = NumberAnswer


class NumberAnswerInput(graphene.InputObjectType):
    id = graphene.ID()
    number_answer = graphene.String(required=True)
    question = graphene.Int(required=True)


class CreateNumberAnswer(graphene.Mutation):
    class Arguments:
        input = NumberAnswerInput(required=True)

    number_answer = graphene.Field(NumberAnswerType)

    @login_required
    def mutate(self, info, input=None):
        if info.context.user.has_perm('survey.can_add_number_answer'):
            if input.number_answer is not None and input.question is not None and info.context.user is not None:
                try:
                    get_question = Question.objects.get(pk=input.question)
                    if get_question.question_type == Question.NUMBER:
                        number_answer_instance = NumberAnswer(number_answer=input.number_answer, question=get_question)
                        number_answer_instance.save()
                        return CreateTextAnswer(number_answer=number_answer_instance)
                    else:
                        raise GraphQLError('Wrong question type!')
                except Question.DoesNotExist:
                    raise GraphQLError('Question does not exist!')
            else:
                raise GraphQLError('Please provide complete information!')
        else:
            raise UnauthorisedAccessError(message='No permissions to create a number answer!')


class UpdateNumberAnswer(graphene.Mutation):
    class Arguments:
        number_answer_id = graphene.Int(required=True)
        input = NumberAnswerInput(required=True)

    text_answer = graphene.Field(TextAnswerType)

    @login_required
    def mutate(self, info, text_answer_id, input=None):
        if info.context.user.has_perm('survey.can_change_text_answer'):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=text_answer_id)
                if text_answer_instance:
                    if input.text_answer:
                        text_answer_instance.text_answer = input.text_answer
                    if input.question:
                        try:
                            get_question = Question.objects.get(pk=input.question)
                            text_answer_instance.question = get_question
                        except Question.DoesNotExist:
                            raise GraphQLError('Question does not exist!')
                    text_answer_instance.save()
                    return UpdateTextAnswer(text_answer=text_answer_instance)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to update a text answer!')


class DeleteTextAnswer(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        text_answer_id = graphene.Int(required=True)

    text_answer = graphene.Field(TextAnswerType)

    @login_required
    def mutate(self, info, text_answer_id):
        if info.context.user.has_perm('survey.can_delete_text_answer'):
            try:
                text_answer_instance = TextAnswer.objects.get(pk=text_answer_id)
                if text_answer_instance:
                    text_answer_instance.delete()
                    return DeleteTextAnswer(ok=True)
            except TextAnswer.DoesNotExist:
                raise GraphQLError('Text answer does not exist!')
        else:
            raise UnauthorisedAccessError(message='No permissions to delete a text answer!')
