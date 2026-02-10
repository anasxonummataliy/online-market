from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    admin_menu = State()


class CategoryState(StatesGroup):
    name = State()


class ProductState(StatesGroup):
    name = State()
    description = State()
    price = State()
    quantity = State()
    image = State()
    category_id = State()


class ChangeCategoryState(StatesGroup):
    name = State()
