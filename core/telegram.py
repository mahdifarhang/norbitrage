from django.conf import settings
import telegram

BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', 'hellow-world')

bot = telegram.Bot(token=BOT_TOKEN)


async def send_telegram_message(message, chat_id):
    await bot.send_message(chat_id=chat_id, text=message)