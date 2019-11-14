from django.db import models
from django.contrib.auth import get_user_model


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    creator = models.ForeignKey(get_user_model(), related_name='boards', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    creator = models.ForeignKey(get_user_model(), related_name='topics', on_delete=models.CASCADE)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(get_user_model(), null=True, related_name='+', on_delete=models.CASCADE)
