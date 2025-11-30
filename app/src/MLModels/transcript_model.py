from typing import Dict

from MLModels.base_model import MLModel
from Audio.audio import AudioFile


class TranscriptionModel(MLModel):
    def predict(self, audio: AudioFile) -> Dict:
        return {
            "transcript": "Hello world",
            "words": 6
        }
