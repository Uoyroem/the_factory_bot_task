from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        related_query_name="message",
    )
    message = models.TextField()
    send_at = models.DateTimeField(auto_now_add=True)


class Token(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tokens",
        related_query_name="token",
    )
    token = models.TextField(default=uuid4)
    telegram_chat_id = models.IntegerField(null=True, blank=True)
