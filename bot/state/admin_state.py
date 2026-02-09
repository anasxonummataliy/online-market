from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    admin_menu = State()
    add_product = State()
    all_product = State()
    add_category = State()
    all_category = State()
