import asyncio
import random
import sys

from sqlalchemy import insert

from api.app.database.database import async_session_maker
from api.app.models.user import User


async def fill_users(n: int):
    print(f"⏳ Генерируем {n} пользователей...")

    users_data = [
        {
            "name": f"User_{i}_{random.randint(1000, 9999)}",
            "email": f"user_{i}_{random.randint(100000, 999999)}@example.com",
            "age": random.randint(18, 80),
        }
        for i in range(n)
    ]

    async with async_session_maker() as session:
        batch_size = 10000
        for i in range(0, len(users_data), batch_size):
            batch = users_data[i : i + batch_size]
            await session.execute(insert(User).values(batch))

        await session.commit()

    print(f"✅ Успешно добавлено {n} пользователей!")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    asyncio.run(fill_users(count))
