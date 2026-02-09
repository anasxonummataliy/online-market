from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    admin_menu = State()


class AddCategoryState(StatesGroup):
    name = State()
