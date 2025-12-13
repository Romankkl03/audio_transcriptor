from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.DataBase.engine import get_session
from src.Thread.thread import ThreadRepository
from .pydantic_models import Thread_api as thread

thread_rout = APIRouter()


@thread_rout.post("/{user_id}/new_threads")
def create_thread(data: thread,
                  session: Session = Depends(get_session)):
    repo = ThreadRepository(session)
    try:
        thread_repo = repo.create_thread(
            user_id=data.user_id,
            audio_name=data.audio_name,
            duration=data.duration,
            content=data.content
        )
        return {
            "thread_id": thread_repo.id,
            "audio_name": thread_repo.audio_name,
            "duration": thread_repo.duration,
            "content": thread_repo.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating thread")


@thread_rout.get("/{user_id}/audios")
def get_all_audio_names(user_id: int,
                        session: Session = Depends(get_session)):
    repo = ThreadRepository(session)
    try:
        audio_names = repo.get_all_audio_names_by_user_id(user_id)
        return {"audio_names": audio_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail="No threads found for user")
