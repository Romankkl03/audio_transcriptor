class User:
    """class User represents a user in the system.
    Attributes:
        _id (int): Unique identifier for the user.
        _email (str): Email address of the user.
        _password (str): Password for the user's account.
        _balance (float): Current balance of credits for the user.
    """
    def __init__(self, user_id: int,
                 email: str,
                 password: str,
                 balance: float = 0.0):
        self._id = user_id
        self._email = email
        self._password = password
        self._balance = balance

    def get_id(self) -> int:
        return self._id
    
    def get_email(self) -> str:
        return self._email
    
    def get_password(self) -> str:
        return self._password
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the user's password.
        Args:
            password (str): The password to check.
        """
        return self._password == password


class AdminUser(User):
    def increase_user_balance(self, user: "User", amount: float) -> None:
        user.increase_balance(amount)
