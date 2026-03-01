# main.py
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import config

from handlers.video_bot import start_video, callback_video
from handlers.music_bot import start_music, callback_music
from handlers.random_bot import start_random, callback_random
from handlers.ads_bot import start_ads, callback_ads

app = ApplicationBuilder().token(config.TOKEN).build()

# Команда /start показывает клавиатуру выбора
app.add_handler(CommandHandler("start", start_video))
app.add_handler(CommandHandler("start", start_music))
app.add_handler(CommandHandler("start", start_random))
app.add_handler(CommandHandler("start", start_ads))

# Callback от inline кнопок
app.add_handler(CallbackQueryHandler(callback_video, pattern="video"))
app.add_handler(CallbackQueryHandler(callback_music, pattern="music"))
app.add_handler(CallbackQueryHandler(callback_random, pattern="random"))
app.add_handler(CallbackQueryHandler(callback_ads, pattern="ads"))

print("Бот запущен...")
app.run_polling()