from django.db import models
from django.contrib.auth import get_user_model


class Survey(models.Model):
    survey_name = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField()
    s_created_on = models.DateTimeField(auto_now=True)
    s_created_by = models.ForeignKey(get_user_model(), related_name='survey_created_by', on_delete=models.CASCADE)
    s_updated_on = models.DateTimeField(auto_now=True)
    s_updated_by = models.ForeignKey(get_user_model(), related_name='survey_updated_by', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publish date')

    def __str__(self):
        return self.survey_name


class Question(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    NUMBER = 'number'

    QTYPES = (
        (TEXT, 'text'),
        (SELECT, 'select'),
        (NUMBER, 'number'),
    )

    question_text = models.CharField(max_length=1000, blank=False, null=False)
    q_created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='question_created_by')
    q_updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='question_updated_by')
    question_type = models.CharField(max_length=200, choices=QTYPES, default=TEXT)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=1000, blank=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    a_created_on = models.DateTimeField(auto_now=True)
    a_created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    a_updated_on = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class TextAnswer(Answer):
    answer_text = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.answer_text


class ChoiceAnswer(Answer):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice.choice_text


class NumberAnswer(Answer):
    number = models.IntegerField(blank=False, null=False)

    def __int__(self):
        return self.number
