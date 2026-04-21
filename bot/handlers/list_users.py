from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from httpx import HTTPStatusError

from bot.services.api_client import api_client

router = Router(name="list_users_router")


class UserPagination(CallbackData, prefix="usr_page"):
    action: str


def get_keyboard(has_prev: bool, has_next: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if has_prev:
        builder.button(text="Назад", callback_data=UserPagination(action="prev"))
    if has_next:
        builder.button(text="Вперед", callback_data=UserPagination(action="next"))
    builder.adjust(2)
    return builder.as_markup()


async def send_users_page(message: types.Message, state: FSMContext, is_edit: bool = False):
    data = await state.get_data()
    cursor_history = data.get("cursor_history", [None])
    current_cursor = cursor_history[-1]

    try:
        paginated_data = await api_client.list_users(cursor=current_cursor, limit=10)

        if not paginated_data.items and current_cursor is None:
            text = "Список пользователей пуст"
            if is_edit:
                await message.edit_text(text=text)
            else:
                await message.answer(text=text)
            return
        await state.update_data(next_cursor=paginated_data.next_cursor)

        lines = ["<b>Список пользователей:</b>"]
        for user in paginated_data.items:
            lines.append(
                f"id: {user.id}, "
                f"name: {user.name}, "
                f"age: {user.age}, "
                f"email: {user.email}, "
                f"created_at: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        text = "\n".join(lines)

        has_prev = len(cursor_history) > 1
        has_next = paginated_data.next_cursor is not None

        keyboard = get_keyboard(has_prev, has_next)

        if is_edit:
            await message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await message.answer(text=text, parse_mode="HTML", reply_markup=keyboard)

    except HTTPStatusError as e:
        err_msg = f"<b>Ошибка API:</b> {e.response.status_code}"
        if is_edit:
            await message.edit_text(text=err_msg, parse_mode="HTML")
        else:
            await message.answer(text=err_msg, parse_mode="HTML")
    except Exception as e:
        err_msg = f"Произошла неизвестная ошибка при загрузке: {str(e)}"
        if is_edit:
            await message.edit_text(err_msg, parse_mode="HTML")
        else:
            await message.answer(err_msg, parse_mode="HTML")


@router.message(Command("list_users"))
async def list_users(message: types.Message, state: FSMContext):
    await state.update_data(cursor_history=[None], next_cursor=None)
    await send_users_page(message=message, state=state, is_edit=False)


@router.callback_query(UserPagination.filter())
async def paginate_users(query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    cursor_history = data.get("cursor_history", [None])

    if callback_data.action == "next":
        next_cursor = data.get("next_cursor")
        if next_cursor:
            cursor_history.append(next_cursor)
            await state.update_data(cursor_history=cursor_history)
    elif callback_data.action == "prev":
        if len(cursor_history) > 1:
            cursor_history.pop()
            await state.update_data(cursor_history=cursor_history)

    await send_users_page(message=query.message, state=state, is_edit=True)
    await query.answer()
