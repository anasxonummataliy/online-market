from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.buttons.sub_menu import ADMIN, BACK_TEXT
from bot.filters.admin import IsAdmin


admin_menu = Router()
admin_menu.message.filter(IsAdmin())


@admin_menu.message(IsAdmin(), F.text == ADMIN)
async def admin_menu_handler(message: Message):
    markup = [
        [KeyboardButton(text=_("Add product")), KeyboardButton(text=_("Show products"))],
        [KeyboardButton(text=_("Add category")), KeyboardButton(text=_("Show categories"))],
        [KeyboardButton(text=str(BACK_TEXT))],
    ]
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer(_("Menu"), reply_markup=rkm.as_markup())
