# utils.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config

def bot_keyboard():
    """Возвращает Inline-клавиатуру для выбора бота"""
    buttons = [
        [InlineKeyboardButton(f"{info['emoji']} {info['name']}", callback_data=key)]
        for key, info in config.BOTS.items()
    ]
    return InlineKeyboardMarkup(buttons)