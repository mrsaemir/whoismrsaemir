import telegram
from django.conf import settings


def send_message(chat_id=settings.OWNER_TELEGRAM_USERNAME, text=None):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    bot.sendMessage(chat_id=chat_id, text=text)

