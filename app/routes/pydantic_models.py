from pydantic import BaseModel


class User_api(BaseModel):
    email: str
    password: str


class Thread_api(BaseModel):
    user_id: int
    audio_name: str
    duration: float
    content: str


class Transaction_api(BaseModel):
    user_id: int
    amount: float
    type: str


class Balance_api(BaseModel):
    user_id: int
    amount: int
