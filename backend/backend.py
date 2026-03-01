from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.bot_utils import send_video
from datetime import datetime
import yt_dlp
import os

app = FastAPI()

# Разрешаем запросы с MiniApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Лимиты пользователей
users_data = {}
MAX_DOWNLOADS = 5
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.post("/video_info")
async def video_info(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    url = data.get("url")
    if not user_id or not url:
        return {"error": "user_id и url обязательны"}

    today = datetime.now().date()
    user = users_data.get(user_id)
    if not user or user["date"] != today:
        users_data[user_id] = {"date": today, "count": 0, "premium": False}

    limit_reached = not users_data[user_id]["premium"] and users_data[user_id]["count"] >= MAX_DOWNLOADS

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
    user_id = data.get("user_id")
    url = data.get("url")
    format_selected = data.get("format", "720")
    extract_music = data.get("extract_music", False)
    bot_name = data.get("bot_name", "video_bot")
    if not url or not user_id:
        return {"error": "user_id и url обязательны"}

    today = datetime.now().date()
    user = users_data.get(user_id)
    if not user or user["date"] != today:
        users_data[user_id] = {"date": today, "count": 0, "premium": False}

    if not users_data[user_id]["premium"] and users_data[user_id]["count"] >= MAX_DOWNLOADS:
        return {"error": "LIMIT_REACHED"}

    ydl_opts = {
        "format": f"bestvideo[height<={format_selected}]+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": True
    }
    if extract_music:
        ydl_opts.update({"format": "bestaudio", "postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "mp3"}]})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
        users_data[user_id]["count"] += 1
        video_path = ydl.prepare_filename(info)
        send_video(bot_name, user_id, video_path, caption=info.get("title", "Видео"))
        return {"status": "OK", "filename": video_path}
    except Exception as e:
        return {"error": str(e)}