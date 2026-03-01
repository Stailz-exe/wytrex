from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
from telegram import Bot
from datetime import datetime

TOKEN = "ВАШ_BOT_TOKEN"
bot = Bot(token=TOKEN)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Render / MiniApp будет работать
    allow_methods=["*"],
    allow_headers=["*"],
)

users_data = {}
MAX_DOWNLOADS = 5

def check_limit(user_id):
    today = datetime.now().date()
    user = users_data.get(user_id)

    if not user:
        users_data[user_id] = {"date": today, "count": 0, "premium": False}
        return True

    if user["date"] != today:
        user["date"] = today
        user["count"] = 0

    if user["premium"]:
        return True

    return user["count"] < MAX_DOWNLOADS

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    url = data["url"]
    format_selected = data["format"]

    if not check_limit(user_id):
        return {"error": "LIMIT_REACHED"}

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': f'bestvideo[height<={format_selected}]+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

        users_data[user_id]["count"] += 1

        await bot.send_video(chat_id=user_id, video=open(filepath, "rb"))

        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}