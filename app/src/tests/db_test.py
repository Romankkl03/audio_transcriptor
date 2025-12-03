from src.DataBase.engine import get_session, engine
from src.DataBase.base import Base
from src.Users.user_repo import UserRepository
from src.Balance.balance import BalanceRepository
from src.Balance.transaction import TransactionRepository
from src.Thread.thread import ThreadRepository


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = get_session()

    users = UserRepository(session)
    balances = BalanceRepository(session)
    transactions = TransactionRepository(session)
    thread = ThreadRepository(session)

    print("Создание пользователя")
    user = users.create_user("test@example.com", "12345")
    print("Пользователь:", user.id, user.email)

    print("Создание баланса")
    balance = balances.create_balance(user.id, 0)
    print("Баланс:", balance.amount)

    print("Пополнение баланса")
    balances.increase_balance(user.id, 150)
    session.refresh(balance)
    print("Баланс:", balance.amount)

    print("Списание баланса")
    balances.decrease_balance(user.id, 20)
    session.refresh(balance)
    print("Баланс:", balance.amount)

    print("Создание транзакций")
    transactions.create_transaction(user.id, 150, "topup")
    transactions.create_transaction(user.id, -20, "spend")

    print("История транзакций")
    history = transactions.get_all_by_user_id(user.id)
    for t in history:
        print(f"Транзакция #{t.id}: {t.amount}, {t.type}, {t.created_at}")
    
    print("История запросов")
    thread.create_thread(user.id, "audio1.mp3", 12.5, "content1")
    thread.create_thread(user.id, "audio2.mp3", 15.0, "content2")
    audio_names = thread.get_all_audio_names_by_user_id(user.id)
    for name in audio_names:
        print("Аудио:", name)

    print("Успешно")
