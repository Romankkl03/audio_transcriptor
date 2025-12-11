from fastapi import APIRouter, HTTPException
from src.DataBase.engine import get_session
from src.Balance.transaction import TransactionRepository
from .pydantic_models import Transaction_api

transaction_rout = APIRouter()


@transaction_rout.post("/{user_id}/create_transaction")
def create_transaction(data: Transaction_api):
    session = get_session()
    repo = TransactionRepository(session)
    try:
        transaction = repo.create_transaction(
            user_id=data.user_id,
            amount=data.amount,
            type=data.type
        )
        return {
            "transaction_id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "type": transaction.type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating transaction")


@transaction_rout.get("/{user_id}/history")
def get_transaction_history(user_id: int):
    session = get_session()
    repo = TransactionRepository(session)
    try:
        transactions = repo.get_all_by_user_id(user_id)
        return {"transactions": [
            {
                "transaction_id": t.id,
                "user_id": t.user_id,
                "amount": t.amount,
                "type": t.type
            } for t in transactions
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="No transactions found for user")
