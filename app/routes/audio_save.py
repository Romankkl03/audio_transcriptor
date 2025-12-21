import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.MQ.producer import publish_task
from pathlib import Path

worker_rout = APIRouter()
AUDIO_DIR = "/app/test_audio"
Path(AUDIO_DIR).mkdir(exist_ok=True)

@worker_rout.post("/transcribation/{user_id}")
async def transcribe_audio(
    user_id: int,
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only mp3 files allowed")

    task_id = str(uuid.uuid4())
    file_path = f"{AUDIO_DIR}/{task_id}.mp3"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    publish_task({
        "task_id": task_id,
        "user_id": user_id,
        "audio_name": file.filename,
        "audio_path": file_path
    })
    return {
        "task_id": task_id,
        "status": "queued"
    }

