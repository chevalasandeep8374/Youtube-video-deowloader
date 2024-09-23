import yt_dlp
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()

def download_youtube_video(video_url, save_path='.'):
    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return {"status": "success", "message": "Download completed!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/download/")
async def download_video(video_url: str = Form(...), save_path: str = Form('./downloads')):
    result = download_youtube_video(video_url, save_path)
    return JSONResponse(content=result)
