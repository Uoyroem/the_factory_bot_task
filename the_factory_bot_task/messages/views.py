from contextlib import suppress
import asyncio

from rest_framework import viewsets, permissions
from aiogram import Bot, executor
from django.conf import settings

from aiogram.utils.exceptions import ValidationError

from . import models, serializers


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = models.Message.objects.all()

    def perform_create(self, serializer):
        message: models.Message = serializer.save(sender=self.request.user)
        with suppress(ValidationError):
            bot = Bot(settings.TELEGRAM_BOT_TOKEN)
            for token in models.Token.objects.filter(user=self.request.user):
                if token.telegram_chat_id is None:
                    continue
                asyncio.run(
                    bot.send_message(
                        token.telegram_chat_id,
                        f"{message.sender.get_full_name()}, я получил от тебя сообщение: \n{message.message}",
                    )
                )


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Token.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
