# backend/backend.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from bot_utils import send_video
import yt_dlp, os
from datetime import datetime
from config import BOTS_CONFIG

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

users_data = {}
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.post("/video_info")
async def video_info(request: Request):
    data = await request.json()
    bot_name = data.get("bot_name")  # video_bot, music_bot...
    user_id = data.get("user_id")
    url = data.get("url")

    if not url or not user_id or not bot_name:
        return {"error": "bot_name, user_id и url обязательны"}

    today = datetime.now().date()
    user = users_data.get((bot_name, user_id))
    if not user or user["date"] != today:
        users_data[(bot_name, user_id)] = {"date": today, "count": 0, "premium": False}

    limit_reached = not users_data[(bot_name, user_id)]["premium"] and users_data[(bot_name, user_id)]["count"] >= 5

    try:
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "N/A"),
            "views": info.get("view_count", 0),
            "likes": info.get("like_count", 0),
            "comments": info.get("comment_count", 0),
            "date": info.get("upload_date", "N/A"),
            "limit_reached": limit_reached
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    bot_name = data.get("bot_name")
    user_id = data.get("user_id")
    url = data.get("url")
    format_selected = data.get("format", "720")
    extract_description = data.get("extract_description", False)
    extract_music = data.get("extract_music", False)

    if not url or not user_id or not bot_name:
        return {"error": "bot_name, user_id и url обязательны"}

    today = datetime.now().date()
    user = users_data.get((bot_name, user_id))
    if not user or user["date"] != today:
        users_data[(bot_name, user_id)] = {"date": today, "count": 0, "premium": False}

    if not users_data[(bot_name, user_id)]["premium"] and users_data[(bot_name, user_id)]["count"] >= 5:
        return {"error": "LIMIT_REACHED"}

    try:
        ydl_opts = {
            "format": f"bestvideo[height<={format_selected}]+bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "quiet": True
        }
        if extract_music:
            ydl_opts.update({
                "format": "bestaudio",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)

        file_path = ydl.prepare_filename(info)
        send_video(bot_name=bot_name, chat_id=user_id, file_path=file_path, caption=info.get("title"))
        users_data[(bot_name, user_id)]["count"] += 1

        return {"status": "OK", "filename": file_path}
    except Exception as e:
        return {"error": str(e)}