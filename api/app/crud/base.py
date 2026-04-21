from typing import Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: int) -> ModelType | None:
        """Получить запись по ID"""
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Получить список всех записей"""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: dict, refresh: bool = False) -> ModelType:
        """Создать запись"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        if refresh:
            await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: dict, refresh: bool = False) -> ModelType:
        """Обновить существующую запись"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        await self.db.flush()
        if refresh:
            await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj) -> None:
        """Удалить объект записи"""
        await self.db.delete(db_obj)
        await self.db.flush()

    async def delete_by_id(self, obj_id: int) -> int | None:
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model.id)
        result = await self.db.execute(query)
        deleted_id = result.scalar_one_or_none()
        return deleted_id
