# backend/config.py

import os
from dotenv import load_dotenv
load_dotenv() 


# Конфиги каждого бота
BOTS_CONFIG = {
    "video_bot": {
        "BOT_TOKEN": os.getenv("8764964206:AAGmiT9eFu4TPbyxzQVx-0hdk-VvRbdUm60"),
        "API_ID": int(os.getenv("39119815")),
        "API_HASH": os.getenv("b60adc78911238a6e125be0aa2267acd"),
        "LOG_CHAT_ID": int(os.getenv("-1003712029427", 0))
    },
    "music_bot": {
        "BOT_TOKEN": os.getenv("MUSIC_BOT_TOKEN"),
        "API_ID": int(os.getenv("MUSIC_API_ID")),
        "API_HASH": os.getenv("MUSIC_API_HASH"),
        "LOG_CHAT_ID": int(os.getenv("MUSIC_LOG_CHAT_ID", 0))
    },
    # Можно добавить любые другие боты
}