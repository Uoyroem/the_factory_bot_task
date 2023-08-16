from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentTypes, Message
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils.translation import gettext as _

from the_factory_bot_task.messages.models import Token


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = Bot(settings.TELEGRAM_BOT_TOKEN, proxy=settings.TELEGRAM_BOT_PROXY)
        dispatcher = Dispatcher(bot)

        @dispatcher.message_handler(commands=["start"])
        async def start_command_handler(message: Message) -> None:
            await message.answer(
                _(
                    f"""Hi.
Here you can link your token generated from {reverse('token-list')} just by sending a text message. 
After linking, you can send messages from {reverse('message-list')}."""
                )
            )

        @dispatcher.message_handler()
        async def text_content_handler(message: Message) -> None:
            try:
                token = await sync_to_async(Token.objects.get)(token=message.text)
            except Token.DoesNotExist:
                await message.answer("Неправильный токен.")
            else:
                if token.chat_id is None:
                    token.chat_id = message.chat.id
                    await sync_to_async(token.save)()
                    await message.answer(
                        f"Токен успешно связан с {await sync_to_async(token.user.get_full_name)()}"
                    )
                else:
                    await message.answer(
                        f"Токен уже связан с {await sync_to_async(token.user.get_full_name)()}."
                    )

        executor.start_polling(dispatcher, skip_updates=True)
