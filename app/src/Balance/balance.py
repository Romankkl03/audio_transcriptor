from src.DataBase.models import Balance

from sqlalchemy.orm import Session


class BalanceRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_balance(self, user_id: int, amount: float = 0.):
        balance = Balance(user_id=user_id, amount=amount)
        self.session.add(balance)
        self.session.commit()
        return balance
    
    def set_balance_by_user_id(self, user_id: int, amount: float):
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount = amount
        self.session.commit()
    
    def decrease_balance(self, user_id: int, amount: float):
        """Decrease the user's balance by the specified amount."""
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount -= amount
        self.session.commit()
    
    def increase_balance(self, user_id: int, amount: float):
        """Increase the user's balance by the specified amount."""
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount += amount
        self.session.commit()
