from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from httpx import HTTPStatusError

from bot.services.api_client import api_client
from bot.states.user_states import DeleteUser

router = Router(name="delete_user_router")


@router.message(Command("delete_user"))
async def delete_user(message: types.Message, state: FSMContext):
    await state.set_state(DeleteUser.waiting_for_id)
    await message.answer(
        "Удаление пользователя\nШаг 1:\nВведите <b>ID пользователя</b>",
        parse_mode="HTML",
    )


@router.message(DeleteUser.waiting_for_id)
async def process_user_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Некорректное значение, <b>ID</b> должно быть числом. Попробуйте еще раз")
        return

    user_id = int(message.text)
    if user_id <= 0:
        await message.answer("Некорректное значение, <b>ID</b> должно быть больше 0. Попробуйте еще раз")
        return

    msg = await message.answer("Удаление пользователя...")
    try:
        await api_client.delete_user(user_id)

        await msg.edit_text("Пользователь успешно удален!")
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}")
    except HTTPStatusError as e:
        await message.answer(f"Ошибка API: {e.response.status_code}")
    finally:
        await state.clear()
