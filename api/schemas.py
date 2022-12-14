from pydantic import BaseModel, EmailStr, UUID4

from datetime import date
from typing import Optional
from project_config import config


class JWTSettings(BaseModel):
    authjwt_secret_key: str = config.secret_key


# Модель для принятия данных для логина
class LoginUserBase(BaseModel):
    username: str
    password: str


# Модель для принятия данных для логина
class UserCreate(LoginUserBase):
    email: Optional[EmailStr]


class User(BaseModel):
    id: UUID4


class UserResponse(User):
    is_authenticated: bool

    class Config:
        orm_mode = True


class UserItem(UserResponse):
    username: str
    name: str
    birth: date
    tg: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True
