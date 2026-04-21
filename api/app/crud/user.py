from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.crud.base import BaseRepository
from api.app.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def get_by_email(self, email: str) -> User | None:
        """Ищем пользователя по email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_cursor(self, cursor: int | None = None, limit: int = 100) -> tuple[list[User], int | None]:
        query = select(User).order_by(User.id)
        if cursor:
            query = query.where(User.id > cursor)

        query = query.limit(limit + 1)
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        next_cursor = None
        if len(items) > limit:
            items = items[:limit]
            next_cursor = items[-1].id

        return items, next_cursor
