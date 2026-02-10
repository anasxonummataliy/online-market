from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

from bot.buttons.sub_menu import ADMIN
from bot.filter.admin import IsAdmin


admin_menu = Router()
admin_menu.message.filter(IsAdmin())


@admin_menu.message(IsAdmin(), F.text == ADMIN)
async def admin_menu_handler(message: Message):
    markup = [
        [KeyboardButton(text="Add product"), KeyboardButton(text="Show products")],
        [KeyboardButton(text="Add category"), KeyboardButton(text="Show categories")],
        [KeyboardButton(text="⏮️ Back")],
    ]
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer("Menu", reply_markup=rkm.as_markup())
