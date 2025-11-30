class Balance:
    def __init__(self, user_id, balance):
        self._user_id = user_id
        self._balance = balance
    
    def get_balance(self) -> float:
        return self._balance
    
    def set_balance(self) -> None:
        return self._balance
    
    def decrease_balance(self, amount: float) -> None:
        """Decrease the user's balance by the specified amount.
        Args:
            amount (float): The amount to decrease from the balance.
        """
        if amount > self._balance:
            raise ValueError("Недостаточно кредитов.")
        self._balance -= amount
    
    def increase_balance(self, amount: float) -> None:
        """Increase the user's balance by the specified amount."""
        self._balance += amount
        