from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons.sub_menu import ADMIN
from bot.filter.admin import IsAdmin

admin_menu = Router()


@admin_menu.message(IsAdmin(), F.text == ADMIN)
async def admin_menu_handler(message: Message):
    markup = [
        [KeyboardButton(text="Add product"), KeyboardButton(text="All product")],
        [KeyboardButton(text="Add category"), KeyboardButton(text="All category")],
    ]
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer("Menu", reply_markup=rkm.as_markup())
