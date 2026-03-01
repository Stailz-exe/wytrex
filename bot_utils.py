# backend/bot_utils.py
from telegram import Bot
from telegram.error import TelegramError
from config import BOTS_CONFIG

def get_bot(bot_name: str):
    cfg = BOTS_CONFIG.get(bot_name)
    if not cfg:
        raise ValueError(f"Бот {bot_name} не найден")
    return Bot(token=cfg["BOT_TOKEN"]), cfg["LOG_CHAT_ID"]

def send_video(bot_name: str, chat_id: int, file_path: str, caption: str = ""):
    bot, log_chat = get_bot(bot_name)
    try:
        with open(file_path, "rb") as f:
            bot.send_video(chat_id=chat_id, video=f, caption=caption)
    except TelegramError as e:
        print(f"[{bot_name}] Ошибка отправки видео: {e}")
        if log_chat:
            bot.send_message(chat_id=log_chat, text=f"[{bot_name}] Ошибка для {chat_id}: {e}")

def send_message(bot_name: str, chat_id: int, text: str):
    bot, log_chat = get_bot(bot_name)
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        print(f"[{bot_name}] Ошибка отправки сообщения: {e}")
        if log_chat:
            bot.send_message(chat_id=log_chat, text=f"[{bot_name}] Ошибка для {chat_id}: {e}")