from fastapi import APIRouter, HTTPException, status, Depends
from src.DataBase.engine import get_session
from sqlalchemy.orm import Session
from .pydantic_models import User_api as User
from src.Users.user_repo import UserRepository
from src.auth.hash_password import HashPassword
from typing import Dict, List

import logging


logger = logging.getLogger(__name__)
user_route = APIRouter()


@user_route.post(
    '/registration',
    description="Register a new user with email and password")
def register_user(data: User,
            session: Session = Depends(get_session)) -> Dict[str, int | str]:
    repo = UserRepository(session)
    existing = repo.get_by_email(data.email)
    try:
        if existing:
            logger.warning(f"Signup attempt with existing email: {data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        user = repo.create_user(data.email, data.password)
        return {"id": user.id, "email": user.email}
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@user_route.post('/auntification', description="Authenticate user and return user ID")
def login(data: User,
          session: Session = Depends(get_session)) -> Dict[str, str | int]:
    repo = UserRepository(session)

    user = repo.get_by_email(data.email)
    if not user:
        logger.warning(f"Login attempt with non-existent email: {data.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    hash_password = HashPassword()
    if hash_password.verify_hash(data.password, user.password) is False:
    # if user.password != data.password:
        logger.warning(f"Failed login attempt for user: {data.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")

    return {"message": "ok", "user_id": user.id}


@user_route.get('/{user_id}/service')
def get_all_users(user_id: int,
                  session: Session = Depends(get_session)
                  ) -> Dict[str, List[Dict[str, int | str]]]:
    repo = UserRepository(session)

    user = repo.get_by_id(user_id)

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation is forbidden."
        )
    
    users = repo.get_all_users()
    return users


@user_route.post('/{user_id}/deletion')
def delete_user(user_id: int,
                session: Session = Depends(get_session)) -> Dict[str, str]:
    repo = UserRepository(session)
    try:
        repo.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
