from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    created_at: datetime


class PaginatedUsersResponseDTO(BaseModel):
    items: list[UserResponseDTO]
    next_cursor: int | None = None
