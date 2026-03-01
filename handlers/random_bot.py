# handlers/random_bot.py
from telegram import Update
from telegram.ext import ContextTypes
from utils import bot_keyboard
import config

async def start_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Выберите бота:",
            reply_markup=bot_keyboard()
        )

async def callback_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_type = query.data
    bot_info = config.BOTS.get(bot_type)
    if bot_info:
        await query.edit_message_text(
            f"✅ Вы выбрали {bot_info['emoji']} {bot_info['name']}!\nТеперь вы можете пользоваться этим ботом."
        )