from typing import Dict

from Audio.audio import AudioFile


class MLModel:
    """ Base class for machine learning models.
    Attributes:
        _model_name (str): Name of the model.
        _unit_price (float): Price per unit of processing. 
        Unit is 10 seconds of audio.
    """
    def __init__(self, model_name: str, unit_price: float):
        self._model_name = model_name
        self._unit_price = unit_price

    def get_name(self) -> str:
        return self._model_name

    def calculate_cost(self, audio: AudioFile) -> float:
        return audio.get_duration() / 10 * self._price_per_unit

    def predict(self, audio: AudioFile) -> Dict:
        pass
