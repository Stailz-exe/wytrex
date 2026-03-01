# handlers/video_bot.py
from telegram import Update
from telegram.ext import ContextTypes
from utils import bot_keyboard
import config
import yt_dlp
import os

async def start_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показываем клавиатуру выбора бота"""
    if update.message:
        await update.message.reply_text(
            "Выберите бота:",
            reply_markup=bot_keyboard()
        )

async def callback_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bot_info = config.BOTS.get(query.data)
    if bot_info:
        await query.edit_message_text(
            f"✅ Вы выбрали {bot_info['emoji']} {bot_info['name']}!\nТеперь вы можете пользоваться этим ботом.\n\n"
            f"Чтобы скачать видео, отправьте команду:\n/download <ссылка на видео>"
        )

# Новая функция для скачивания видео
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not context.args:
        await message.reply_text("❌ Пожалуйста, укажите ссылку на видео.\nПример: /download https://youtube.com/...")
        return

    url = context.args[0]
    await message.reply_text("⏳ Скачиваем видео, подождите...")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Конвертация в mp4 через ffmpeg
    }

    os.makedirs('downloads', exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
        await message.reply_text(f"✅ Видео скачано: {os.path.basename(filepath)}")
    except Exception as e:
        await message.reply_text(f"❌ Ошибка при скачивании: {e}")