from aiogram.fsm.state import State, StatesGroup


class CreateUser(StatesGroup):
    """Команда /create_user"""

    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_age = State()


class DeleteUser(StatesGroup):
    """Команда /delete_user"""

    waiting_for_id = State()
