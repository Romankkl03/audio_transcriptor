from src.DataBase.models import Balance

from sqlalchemy.orm import Session


class BalanceRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_balance(self, user_id: int, amount: int = 0):
        balance = Balance(user_id=user_id, amount=amount)
        self.session.add(balance)
        self.session.commit()
        return balance

    def get_by_user_id(self, user_id: int):
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        return balance

    def set_balance_by_user_id(self, user_id: int, amount: int):
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount = amount
        self.session.commit()
    
    def decrease_balance(self, user_id: int, amount: int):
        """Decrease the user's balance by the specified amount."""
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount -= amount
        self.session.commit()
    
    def increase_balance(self, user_id: int, amount: int):
        """Increase the user's balance by the specified amount."""
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        balance.amount += amount
        self.session.commit()
    
    def has_enough_credits(self, user_id: int, price: int):
        balance = self.session.query(Balance).filter(Balance.user_id == user_id).first()
        return price <= balance.amount
