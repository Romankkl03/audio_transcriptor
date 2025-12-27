from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.DataBase.engine import get_session
from src.Thread.thread import ThreadRepository
from src.Balance.balance import BalanceRepository
from .pydantic_models import Thread_api as thread

thread_rout = APIRouter()


@thread_rout.post("/{user_id}/predictions")
async def save_transcription(
    user_id: int,
    data: thread,
    session: Session = Depends(get_session)
):
    repo_preds = ThreadRepository(session)
    repo_balance = BalanceRepository(session)

    try:
        cost = int(data.duration) * 10
        if not repo_balance.has_enough_credits(data.user_id, cost):
            raise HTTPException(
                status_code=402,
                detail="Not enough balance"
            )

        thread_repo = repo_preds.create_thread(
            user_id=data.user_id,
            audio_name=data.audio_name,
            duration=data.duration,
            content=data.content
        )

        repo_balance.decrease_balance(
            user_id=data.user_id,
            amount=cost
        )
        session.commit()

        return {
            "thread_id": thread_repo.id,
            "audio_name": thread_repo.audio_name,
            "duration": thread_repo.duration,
            "content": thread_repo.content
        }

    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@thread_rout.get("/{user_id}/threads")
def get_threads(
    user_id: int,
    session: Session = Depends(get_session)
):
    repo = ThreadRepository(session)
    threads = repo.get_threads_by_user_id(user_id)
    if len(threads) > 0:
        return [
            {
                "id": t.id,
                "audio_name": t.audio_name,
                "duration": t.duration,
                "content": t.content,
                "created_at": t.created_at
            }
            for t in threads
        ]
    else:
        return "No transcripts yet!"

@thread_rout.get("/{user_id}/{thread_id}")
def get_current_thread(
    user_id: int,
    thread_id: int,
    session: Session = Depends(get_session)
):
    repo = ThreadRepository(session)
    threads = repo.get_thread_by_id(thread_id)
    return {
            "id": threads.id,
            "audio_name": threads.audio_name,
            "duration": threads.duration,
            "content": threads.content,
            "created_at": threads.created_at
        }

@thread_rout.get("/{user_id}/audios")
def get_all_audio_names(user_id: int,
                        session: Session = Depends(get_session)):
    repo = ThreadRepository(session)
    try:
        audio_names = repo.get_all_audio_names_by_user_id(user_id)
        return {"audio_names": audio_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail="No threads found for user")
