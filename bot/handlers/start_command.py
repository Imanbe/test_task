from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router(name="start_router")


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "Меню команд:\n"
        "/create_user - создание пользователя\n"
        "/delete_user - удаление пользователя\n"
        "/list_users - список пользователей"
    )
