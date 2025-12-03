from .engine import engine, get_session
from .models import Base, User, Balance, Transaction

from logging import getLogger

logger = getLogger(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = get_session()

    if session.query(User).first():
        logger.info("Database already initialized.")
        session.close()
        return

    user = User(
        email="user@user.ru",
        password="user123",
        role="user",
    )
    session.add(user)
    session.flush()

    session.add(Balance(user_id=user.id, credits=100))

    session.add(
        Transaction(
            user_id=user.id,
            amount=100,
            type="deposit"
        )
    )

    admin = User(
        email="admin@admin.com",
        assword="admin123",
        role="admin",
    )
    session.add(admin)
    session.flush()

    session.add(Balance(user_id=admin.id, credits=9999))

    session.add(
        Transaction(
            user_id=admin.id,
            amount=9999,
            type="deposit"
        )
    )

    session.commit()
    session.close()

    logger.info("Database initialized with default users.")


if __name__ == "__main__":
    init_db()