from src.DataBase.models import Transaction

from sqlalchemy.orm import Session


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_transaction(self, user_id: int, amount: float, type: str):
        transaction = Transaction(user_id=user_id, amount=amount, type=type)
        self.session.add(transaction)
        self.session.commit()
        return transaction

    def get_transaction_by_id(self, id: int):
        transaction = self.session.query(Transaction).filter(Transaction.id == id).first()
        return transaction

    def get_all_by_user_id(self, user_id: int):
        transactions = self.session.query(Transaction).filter(Transaction.user_id == user_id).all()
        return transactions
