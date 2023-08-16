import asyncio

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from aiogram import Bot
from django.conf import settings
from django.utils.translation import gettext as _


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
                status.HTTP_400_BAD_REQUEST,
            )
        token = None
        try:
            token: models.Token = self.request.user.token
        except models.Token.DoesNotExist:
            raise APIException(
                _("You don't have a token."),
                status.HTTP_400_BAD_REQUEST,
            )
        if token.chat_id is None:
            raise APIException(
                _("You haven't linked the token to the bot."),
                status.HTTP_400_BAD_REQUEST,
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

    @action(detail=False)
    def my_token(self, request: Request) -> Response:
        try:
            token = models.Token.objects.get(user=self.request.user)
        except models.Token.DoesNotExist:
            raise APIException(_("You don't have a token."), status.HTTP_404_NOT_FOUND)
        else:
            serailizer = serializers.TokenSerializer(token)
            return Response(serailizer.data)

    def perform_create(self, serializer):
        try:
            models.Token.objects.get(user=self.request.user)
        except models.Token.DoesNotExist:
            serializer.save(user=self.request.user)
        else:
            raise APIException(
                _("You have already created a token."), status.HTTP_400_BAD_REQUEST
            )
