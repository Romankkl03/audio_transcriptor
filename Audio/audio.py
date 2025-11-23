class AudioFile:
    def __init__(self, file_id: int,
                 user_id: int,
                 filename: str,
                 duration_sec: float,
                 sample_rate: int,
                 language: str=None):
        self._file_id = file_id
        self._user_id = user_id
        self._filename = filename
        self._duration = duration_sec
        self._sample_rate = sample_rate
        self._language = language
        self.detect_lang = False
        if isinstance(self._language, None):
            self.detect_lang = True

    def is_valid_format(self) -> bool:
        return self._filename.endswith((".wav", ".mp3", ".m4a"))

    def get_duration(self) -> float:
        return self._duration_sec

    def get_user_id(self) -> int:
        return self._user_id
    