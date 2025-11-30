from typing import Optional
from Users.user import User
from Users.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: "UserRepository"):
        self._user_repo = user_repo

    def register(self, email: str, password: str) -> User:
        return self._user_repo.create_user(email, password)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self._user_repo.get_by_email(email)
        return user if user and user.check_password(password) else None
