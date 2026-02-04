from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.sub_menu import *
from database.models import Category, Product

product_router = Router()


@product_router.message(F.text == CATEGORIES)
async def get_all_categories(message: Message):
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories != []:
        for category in categories:
            ikm.add(
                InlineKeyboardButton(
                    text=category.name, callback_data=f"category_{category.id}"
                )
            )
        ikm.adjust(2)
        await message.answer("Categories", reply_markup=ikm.as_markup())
    else:
        await message.answer("No categories")

@product_router.callback_query(F.startswith('category_'))
async def callback_categories(callback: CallbackQuery):
    cateogry_id = callback.data.removeprefix("category_")
    products = Product.filter(cateogry_id)
    ikm = InlineKeyboardBuilder()
    for product in products:
        ikm.add(
            InlineKeyboardButton(
                text=product.name, callback_data=f"product_{product.id}"
            )
        )
    ikm.adjust(2)
