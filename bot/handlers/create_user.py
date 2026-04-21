from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from httpx import HTTPStatusError

from bot.schemas.user import UserCreateDTO
from bot.services.api_client import api_client
from bot.states.user_states import CreateUser

router = Router(name="create_user_router")


@router.message(Command("create_user"))
async def cmd_create_user(message: types.Message, state: FSMContext):
    await state.set_state(CreateUser.waiting_for_name)
    await message.answer("Создание пользователя\nШаг 1:\nВведите Имя", parse_mode="HTML")


@router.message(CreateUser.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateUser.waiting_for_email)
    await message.answer("Принято!\nШаг 2:\nВведите Email", parse_mode="HTML")


@router.message(CreateUser.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    if "@" not in message.text:
        await message.answer("Некорректное значение Email. Попробуйте еще раз")
        return

    await state.update_data(email=message.text)
    await state.set_state(CreateUser.waiting_for_age)
    await message.answer("Принято!\nШаг 3:\nВведите Возраст", parse_mode="HTML")


@router.message(CreateUser.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз")
        return
    age = int(message.text)
    if age < 1:
        await message.answer("Возраст должен быть больше 1 года. Попробуйте ещё раз")
        return
    await state.update_data(age=age)
    user_data = await state.get_data()
    payload = UserCreateDTO(**user_data)

    try:
        msg = await message.answer("Идет сохранение в базу данных...")

        user = await api_client.create_user(payload=payload)

        await msg.edit_text(
            f"Пользователь успешно создан!\nID: {user.id}\nИмя: {user.name}\nEmail: {user.email}",
            parse_mode="HTML",
        )
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}")
    except HTTPStatusError as e:
        await message.answer(f"Ошибка API: {e.response.status_code}")
    finally:
        await state.clear()
