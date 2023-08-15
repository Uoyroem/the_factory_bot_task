from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import executor, Bot, Dispatcher
from aiogram.types import Message
from asgiref.sync import sync_to_async


from the_factory_bot_task.messages.models import Token


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = Bot(settings.TELEGRAM_BOT_TOKEN, proxy=settings.TELEGRAM_BOT_PROXY)
        dispatcher = Dispatcher(bot)

        @dispatcher.message_handler()
        async def _(message: Message) -> None:
            try:
                token = await sync_to_async(Token.objects.get)(token=message.text)
            except Token.DoesNotExist:
                await message.answer("Invalid token.")
            else:
                token.telegram_chat_id = message.chat.id
                await sync_to_async(token.save)()
                await message.answer("Successful binding token.")

        executor.start_polling(dispatcher, skip_updates=True)
