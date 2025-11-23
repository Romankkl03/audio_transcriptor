from typing import Optional
from Users.user import User


class UserRepository:
    def create_user(self, email: str, password: str) -> User:
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        pass
