from api.app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from api.app.schemas.user import PaginatedUserResponse, UserCreate, UserResponse
from api.app.uow.unit_of_work import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_users_paginated(self, cursor: int | None, limit: int) -> PaginatedUserResponse:
        async with self.uow:
            items, next_cursor = await self.uow.user_repo.get_all_cursor(cursor=cursor, limit=limit)
            return PaginatedUserResponse(items=items, next_cursor=next_cursor)

    async def create_user(self, payload: UserCreate) -> UserResponse:
        async with self.uow:
            existing_user = await self.uow.user_repo.get_by_email(str(payload.email))
            if existing_user:
                raise UserAlreadyExistsError("Пользователь с таким email уже существует")

            user = await self.uow.user_repo.create(payload.model_dump())
            await self.uow.commit()
            return user

    async def delete_user(self, user_id: int) -> None:
        async with self.uow:
            user = await self.uow.user_repo.get(id=user_id)
            if not user:
                raise UserNotFoundError("Пользователь не найден")

            await self.uow.user_repo.delete(user)
            await self.uow.commit()
