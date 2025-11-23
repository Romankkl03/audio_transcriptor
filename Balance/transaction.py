from datetime import datetime


class BalanceTransaction:
    """ Class representing a balance transaction.
    Attributes:
        _tx_id (int): Unique identifier for the transaction.
        _user_id (int): Identifier of the user associated with the transaction.
        _amount (float): Amount of the transaction.
    """
    def __init__(self, tx_id: int, user_id: int, amount: float):
        self._tx_id = tx_id
        self._user_id = user_id
        self._amount = amount
        self._timestamp = datetime.utcnow()

    def get_amount(self) -> float:
        return self._amount

    def get_user_id(self) -> int:
        return self._user_id
