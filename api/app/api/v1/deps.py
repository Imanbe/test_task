from fastapi import Depends

from api.app.services import UserService
from api.app.uow import AbstractUnitOfWork, SQLAlchemyUnitOfWork


async def get_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork()


async def get_user_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> UserService:
    return UserService(uow=uow)
