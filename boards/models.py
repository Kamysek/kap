from django.db import models
from django.contrib.auth import get_user_model


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    creator = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("view_creator_board", "View board creator"),
        )


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    creator = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("view_creator_topic", "View topic creator"),
        )


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(get_user_model(), null=True, blank=False, related_name='posts_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=False, related_name='posts_updated_by', on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("view_created_by", "View created by"),
            ("view_updated_by", "View updated by"),
        )
