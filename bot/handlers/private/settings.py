from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.sub_menu import SETTINGS
from bot.handlers.private.menu import start_handler

settings_router = Router()


@settings_router.message(F.text == SETTINGS)
async def settings_handler(message: Message):
    markup = [
        [
            KeyboardButton(text=_("Change language 🇬🇧 🇺🇿")),
            KeyboardButton(text=_("Notification 📢")),
        ],
        [KeyboardButton(text=_("⏮️ Back"))],
    ]
    kb = ReplyKeyboardBuilder(markup)
    await message.answer(_("Settings"), reply_markup=kb.as_markup())


@settings_router.message(F.text == _("⏮️ Back"))
async def settings_handler(message: Message):
    await start_handler(message)
