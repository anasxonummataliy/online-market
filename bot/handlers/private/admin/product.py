from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.config import conf
from bot.filter.admin import IsAdmin
from bot.handlers.private import start_handler
from database.models import Category
from bot.state import AdminState, AddCategoryState

admin_product = Router()
admin_product.message.filter(IsAdmin())


@admin_product.message(F.text == "Add category")
async def add_category(message: Message, state: FSMContext):
    await state.set_state(AddCategoryState.name)
    rkm = ReplyKeyboardRemove()
    await message.answer("Enter category name.", reply_markup=rkm)


@admin_product.message(AddCategoryState.name)
async def add_category_name(message: Message, state: FSMContext):
    category_name = message.text
    await Category.create(name=category_name)
    await state.clear()
    await message.answer("Category added successfully.")
    await start_handler(message)
