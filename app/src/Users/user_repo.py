from src.DataBase.models import User, Balance, Transaction
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, email: str, password: str, role: str = "user"):
        user = User(email=email, password=password, role=role)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()
        return user

    def get_by_id(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        return user

    def check_password(self, user_id: int, password: str) -> bool:
        """Check if the provided password matches the user's password.
        """
        user = self.session.query(User).filter(User.id == user_id).first()
        return user.password == password
    
    def get_all_users(self):
        users = self.session.query(User).all()
        return {"users": [{"id": user.id, "email": user.email} for user in users]}
    
    def delete_user(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
