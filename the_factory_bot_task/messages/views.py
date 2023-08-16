import asyncio

from rest_framework import viewsets, permissions
from rest_framework.exceptions import APIException, NotFound
from aiogram import Bot
from django.conf import settings
from django.utils.translation import gettext_lazy as _


import aiogram.utils.exceptions

from . import models, serializers


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = models.Message.objects.all()

    def perform_create(self, serializer):
        message: models.Message = serializer.save(sender=self.request.user)
        try:
            bot = Bot(settings.TELEGRAM_BOT_TOKEN, proxy=settings.TELEGRAM_BOT_PROXY)
        except aiogram.utils.exceptions.ValidationError:
            raise APIException(
                _("The bot token was not specified."),
                400,
            )

        token: models.Token = self.request.user.token
        if token is None or token.chat_id is None:
            raise APIException(
                _("You don't have a token or you haven't linked the token to the bot."),
                400,
            )
        asyncio.run(
            bot.send_message(
                token.chat_id,
                f"{message.sender.get_full_name()}, я получил от тебя сообщение: \n{message.message}",
            )
        )


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Token.objects.all()

    def perform_create(self, serializer):
        try:
            models.Token.objects.get(user=self.request.user)
        except models.Token.DoesNotExist:
            serializer.save(user=self.request.user)
        else:
            raise APIException(_("You have already created a token"), 400)
