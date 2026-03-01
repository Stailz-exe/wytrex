from fastapi import FastAPI, Request
import yt_dlp
from datetime import datetime

app = FastAPI()
users_data = {}
MAX_DOWNLOADS = 5

@app.post("/video_info")
async def video_info(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    url = data["url"]
    today = datetime.now().date()
    user = users_data.get(user_id)
    if not user or user["date"] != today:
        users_data[user_id] = {"date": today, "count": 0, "premium": False}
    limit_reached = not users_data[user_id]["premium"] and users_data[user_id]["count"] >= MAX_DOWNLOADS
    try:
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "views": info.get("view_count", 0),
            "likes": info.get("like_count", 0),
            "comments": info.get("comment_count", 0),
            "date": info.get("upload_date", "N/A"),
            "limit_reached": limit_reached
        }
    except Exception as e:
        return {"error": str(e)}