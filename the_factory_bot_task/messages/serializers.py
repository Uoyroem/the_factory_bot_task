from rest_framework import serializers
from . import models


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["id", "sender", "message", "send_at"]
        read_only_fields = ["sender", "send_at"]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Token
        fields = ["id", "token", "telegram_chat_id", "user"]
        read_only_fields = ["user", "telegram_chat_id", "token"]
