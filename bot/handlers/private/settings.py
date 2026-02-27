from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _, get_i18n

from bot.buttons.sub_menu import (
    ADMIN,
    BACK_TEXT,
    CHANGE_LANG,
    NOTIF,
    SETTINGS,
)
from bot.handlers.private.menu import start_handler

settings_router = Router()


@settings_router.message(F.text == SETTINGS)
async def settings_handler(message: Message):
    markup = [
        [
            KeyboardButton(text=str(CHANGE_LANG)),
            KeyboardButton(text=str(NOTIF)),
        ],
        [KeyboardButton(text=str(BACK_TEXT))],
    ]
    kb = ReplyKeyboardBuilder(markup)
    await message.answer(_("Settings"), reply_markup=kb.as_markup())


@settings_router.message(F.text == BACK_TEXT)
async def back_to_start(message: Message, state: FSMContext):
    await start_handler(message, state)


@settings_router.message(F.text == NOTIF)
async def notif_handler(message: Message):
    pass
