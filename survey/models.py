from django.db import models
from account.models import CustomUser


class Survey(models.Model):
    survey_name = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publish date')

    def __str__(self):
        return self.survey_name


class Question(models.Model):
    T = 'text'
    C = 'choice'
    N = 'number'

    TYPES = (
        (T, 'text'),
        (C, 'choice'),
        (N, 'number'),
    )

    question_text = models.CharField(max_length=1000, blank=False, null=False)
    question_type = models.CharField(max_length=200, choices=TYPES, default=T)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)


class TextAnswer(Answer):
    answer_text = models.TextField(blank=False, null=False)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text


class ChoiceAnswer(Answer):
    choice_text = models.CharField(max_length=1000, blank=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class NumberAnswer(Answer):
    number = models.IntegerField(blank=False, null=False)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    def __int__(self):
        return self.number
