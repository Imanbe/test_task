from datetime import datetime

from pydantic import EmailStr

from api.app.schemas import BaseSchema


class UserBase(BaseSchema):
    name: str
    email: EmailStr
    age: int


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime


class PaginatedUserResponse(BaseSchema):
    items: list[UserResponse]
    next_cursor: int | None = None
