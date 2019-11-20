from django.db import models
from django.contrib.auth import get_user_model


class Survey(models.Model):
    survey_name = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), related_name='survey_created_by', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), related_name='survey_updated_by', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publish date')

    def __str__(self):
        return self.survey_name


class Question(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    NUMBER = 'number'

    QTYPES = (
        (TEXT, 'text'),
        (CHOICE, 'choice'),
        (NUMBER, 'number'),
    )

    question_text = models.CharField(max_length=1000, blank=False, null=False)
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='question_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='question_updated_by')
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
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class TextAnswer(Answer):
    text_answer = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.text_answer


class ChoiceAnswer(Answer):
    choice_answer = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_answer.choice_text


class NumberAnswer(Answer):
    number_answer = models.IntegerField(blank=False, null=False)

    def __int__(self):
        return self.number_answer
