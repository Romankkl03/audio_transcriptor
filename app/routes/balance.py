from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.DataBase.engine import get_session
from src.Balance.balance import BalanceRepository
from .pydantic_models import Balance_api

balance_rout = APIRouter()


@balance_rout.post("/{user_id}/new_balance")
def create_balance(data: Balance_api,
                   session: Session = Depends(get_session)):
    repo = BalanceRepository(session)
    balance = repo.create_balance(data.user_id, data.amount)
    return {"balance_id": balance.id, "user_id": balance.user_id, "amount": balance.amount}


@balance_rout.post("/admin/balances")
def set_balance(data: Balance_api,
                session: Session = Depends(get_session)):
    repo = BalanceRepository(session)
    repo.set_balance_by_user_id(data.user_id, data.amount)
    balance = repo.get_by_user_id(data.user_id)
    return {"balance": balance.amount}


@balance_rout.get("/{user_id}/balances")
def get_balance(user_id: int,
                session: Session = Depends(get_session)):
    repo = BalanceRepository(session)
    balance = repo.get_by_user_id(user_id)
    # If balance does not exist, create one with 0 amount
    # it will happen when user logs in for the first time
    if not balance:
        repo.create_balance(user_id, 0)
        balance = repo.get_by_user_id(user_id)
    return {"balance": balance.amount}


@balance_rout.post("/{user_id}/credit")
def increase_balance(data: Balance_api,
                     session: Session = Depends(get_session)):
    repo = BalanceRepository(session)
    repo.increase_balance(data.user_id, data.amount)
    balance = repo.get_by_user_id(data.user_id)
    return {"balance": balance.amount}


@balance_rout.post("/{user_id}/debit")
def decrease_balance(data: Balance_api,
                     session: Session = Depends(get_session)):
    repo = BalanceRepository(session)
    repo.decrease_balance(data.user_id, data.amount)
    balance = repo.get_by_user_id(data.user_id)
    return {"balance": balance.amount}
