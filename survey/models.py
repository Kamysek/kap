from django.db import models
from django.contrib.auth import get_user_model


class Survey(models.Model):
    survey_name = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), null=True, blank=False, related_name='survey_created_by', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=False, related_name='survey_updated_by', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publish date')

    def __str__(self):
        return self.survey_name

    class Meta:
        permissions = (
            ("view_created_by_survey", "View created by survey"),
            ("view_updated_by_survey", "View updated by survey"),
        )


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
    created_by = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE, related_name='question_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE, related_name='question_updated_by')
    question_type = models.CharField(max_length=200, choices=QTYPES, default=TEXT)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    class Meta:
        permissions = (
            ("view_created_by_question", "View created by survey question"),
            ("view_updated_by_question", "View updated by survey question"),
        )


class Choice(models.Model):
    choice_text = models.CharField(max_length=1000, blank=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("view_created_by_answer", "View created by survey answer"),
            ("view_updated_by_answer", "View updated by survey answer"),
        )


class TextAnswer(Answer):
    text_answer = models.TextField(blank=False, null=True)

    def __str__(self):
        return self.text_answer

    class Meta:
        permissions = (
            ("view_text_answer", "View text answer survey"),
        )


class ChoiceAnswer(Answer):
    choice_answer = models.ForeignKey(Choice, blank=False, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_answer.choice_text

    class Meta:
        permissions = (
            ("view_choice_answer", "View choice answer survey"),
        )


class NumberAnswer(Answer):
    number_answer = models.IntegerField(blank=False, null=True)

    def __int__(self):
        return self.number_answer

    class Meta:
        permissions = (
            ("view_number_answer", "View number answer survey"),
        )
