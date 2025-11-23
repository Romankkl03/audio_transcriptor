from typing import Dict

from MLModels.base_model import MLModel
from Audio.audio import AudioFile

class LanguageDetectionModel(MLModel):
    def predict(self, audio: AudioFile) -> Dict:
        return {
            "language": "en",
            "confidence": 0.9
        }
