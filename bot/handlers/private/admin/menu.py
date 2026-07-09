from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.filters.admin import IsAdmin


admin_menu = Router()
admin_menu.message.filter(IsAdmin())
admin_menu.callback_query.filter(IsAdmin())


def admin_main_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("Add product 📂")), KeyboardButton(text=_("Show products 📂"))],
            [KeyboardButton(text=_("Add category 📂")), KeyboardButton(text=_("Show categories 📂"))],
            [KeyboardButton(text=_("⏮️ Back"))],
        ],
        resize_keyboard=True,
    )


@admin_menu.message(F.text == __("Admin 🧑‍💼"))
async def admin_menu_handler(message: Message):
    await message.answer(_("Menu"), reply_markup=admin_main_markup())


@admin_menu.message(F.text == __("⏮️ Back"))
async def back_handler(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=_("Admin 🧑‍💼"))]],
        resize_keyboard=True,
    )
    await message.answer(_("Main menu"), reply_markup=markup)
