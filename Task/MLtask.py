from datetime import datetime
from typing import Optional, Dict

from Audio.audio import AudioFile
from MLModels.base_model import MLModel


class PredictionResult:
    def __init__(self, task_id: int, output: Dict, cost: float):
        self._task_id = task_id
        self._output = output
        self._cost = cost
        self._created_at = datetime.utcnow()

    def as_dict(self) -> Dict:
        return {
            "task_id": self._task_id,
            "output": self._output,
            "cost": self._cost,
            "created_at": str(self._created_at)
        }


class PredictionTask:
    def __init__(self, task_id: int, user_id: int, audio: AudioFile, model: MLModel):
        self._task_id = task_id
        self._user_id = user_id
        self._audio = audio
        self._model = model
        self._created_at = datetime.utcnow()
        self._status = "created"
        self._result: Optional[PredictionResult] = None

    def start(self):
        self._status = "running"

    def complete(self, result: "PredictionResult"):
        self._status = "completed"
        self._result = result

    def fail(self, error: str):
        # TODO: log the error
        self._status = "failed"

    def get_cost(self) -> float:
        return self._model.calculate_cost(self._audio)

    def get_status(self) -> str:
        return self._status

    def get_result(self) -> Optional["PredictionResult"]:
        return self._result
