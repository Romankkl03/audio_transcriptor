from src.DataBase.models import AudioScript

from sqlalchemy.orm import Session


class ThreadRepository:
    """Repository class for managing user threads in the database."""
    def __init__(self, session: Session):
        self.session = session

    def create_thread(self, 
                      user_id: int,
                      audio_name: str = "audio_script.mp3",
                      duration: float = 0.0,
                      content: str = "bla"):
        thread = AudioScript(
            user_id=user_id,
            audio_name=audio_name,
            duration=duration,
            content=content
        )
        self.session.add(thread)
        self.session.commit()
        return thread
    
    def get_all_audio_names_by_user_id(self, user_id: int):
        threads = self.session.query(AudioScript).filter(AudioScript.user_id == user_id).all()
        return [thread.audio_name for thread in threads]
