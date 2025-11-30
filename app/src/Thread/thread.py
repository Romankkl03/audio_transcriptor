class UserTread:
    """Class representing a user thread.
    Attributes:
        _id (int): Unique identifier for the thread.
        _user_id (int): Identifier of the user who owns the thread.
        _language (str): Language of the first Audio.
    """
    def __init__(self, user_id: int, thread_id: int = None, landuage: str = None):
        self._id = thread_id
        self._user_id = user_id
        self._language = landuage
    
    def create_thread(self) -> None:
        pass
    
    def get_thread_by_id(self) -> int:
        pass
