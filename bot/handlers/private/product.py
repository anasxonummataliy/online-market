from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.sub_menu import *
from database.models import Category
from database.models.shops import Category

product_router = Router()


@product_router.message(F.text == CATEGORIES)
async def get_all_categories(message: Message):
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    for category in categories:
        ikm.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"category_{category.id}"
            )
        )
    await message.answer("Categories", reply_markup=ikm.as_markup())

@product_router.callback_query(F.startswith('category_'))
async def callback_categories(callback: CallbackQuery):
    cateogry_id = callback.data.removeprefix("category_")
    