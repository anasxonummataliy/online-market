from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.sub_menu import (
    BACK_TEXT,
    CHANGE_LANG,
    NOTIF,
    SETTINGS,
)
from bot.handlers.private.menu import start_handler

settings_router = Router()


@settings_router.message(F.text == __(SETTINGS))
async def settings_handler(message: Message):
    markup = [
        [
            KeyboardButton(text=_(CHANGE_LANG)),
            KeyboardButton(text=_(NOTIF)),
        ],
        [KeyboardButton(text=_(BACK_TEXT))],
    ]
    kb = ReplyKeyboardBuilder(markup)
    await message.answer(_("Settings"), reply_markup=kb.as_markup(resize_keyboard=True))


@settings_router.message(F.text == __(BACK_TEXT))
async def back_to_start(message: Message, state: FSMContext):
    await start_handler(message, state)


@settings_router.message(F.text == __(NOTIF))
async def notif_handler(message: Message):
    await message.answer(_("🔔 You don’t have any notifications yet."))
