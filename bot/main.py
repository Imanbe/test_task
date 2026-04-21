import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import settings
from bot.handlers.create_user import router as create_user_router
from bot.handlers.delete_user import router as delete_user_router
from bot.handlers.list_users import router as list_users_router
from bot.handlers.start_command import router as start_command_router
from bot.services.api_client import api_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def main():
    bot = Bot(token=settings.BOT_TOKEN)

    storage = RedisStorage.from_url(settings.REDIS_URL)
    dp = Dispatcher(storage=storage)

    dp.include_router(start_command_router)
    dp.include_router(create_user_router)
    dp.include_router(list_users_router)
    dp.include_router(delete_user_router)

    @dp.startup()
    async def startup():
        logging.info("Бот запущен")

    @dp.shutdown()
    async def shutdown():
        logging.info("Остановка бота")
        await api_client.close()
        await storage.close()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот выключен вручную")
