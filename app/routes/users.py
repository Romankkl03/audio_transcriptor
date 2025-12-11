from fastapi import APIRouter, HTTPException, status
from src.DataBase.engine import get_session
from .pydantic_models import User_api as User
from src.Users.user_repo import UserRepository
from typing import Dict, List

import logging


logger = logging.getLogger(__name__)
user_route = APIRouter()


@user_route.post(
    '/signup',
    description="Register a new user with email and password")
def register_user(data: User) -> Dict[str, int | str]:
    session = get_session()
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


@user_route.post('/signin')
def login(data: User) -> Dict[str, str | int]:
    session = get_session()
    repo = UserRepository(session)

    user = repo.get_by_email(data.email)
    if not user:
        logger.warning(f"Login attempt with non-existent email: {data.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if user.password != data.password:
        logger.warning(f"Failed login attempt for user: {data.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")

    return {"message": "ok", "user_id": user.id}


@user_route.get('/service')
def get_all_users() -> Dict[str, List[Dict[str, int | str]]]:
    session = get_session()
    repo = UserRepository(session)
    users = repo.get_all_users()
    return users


@user_route.post('/{user_id}/delete')
def delete_user(user_id: int) -> Dict[str, str]:
    session = get_session()
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


# @user_route.get(
#     "/get_all_users", 
#     response_model=List[User],
#     summary="Get all users",
#     response_description="List of all users"
# )
# async def get_all_users(session=Depends(get_session)) -> List[User]:
#     """
#     Get list of all users.

#     Args:
#         session: Database session

#     Returns:
#         List[UserResponse]: List of users
#     """
#     try:
#         repo = UserRepository(session)
#         users = repo.get_all_users()
#         users = UserService.get_all_users(session)
#         logger.info(f"Retrieved {len(users)} users")
#         return users
#     except Exception as e:
#         logger.error(f"Error retrieving users: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error retrieving users"
#         )
