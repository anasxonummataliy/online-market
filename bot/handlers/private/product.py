from aiogram import Router, Bot, F
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.sub_menu import *
from database.models import Categoi
from database.models.shops import Category

product_router = Router()

@product_router.message(F.text == CATEGORIES)
async def get_all_categories(message: Message):
    categories = Category.get_all()
