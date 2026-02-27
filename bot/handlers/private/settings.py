from aiogram import Router, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
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


@settings_router.message(F.text == str(SETTINGS))
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


@settings_router.message(F.text == str(BACK_TEXT))
async def back_to_start(message: Message):
    await start_handler(message)


@settings_router.message(F.text == NOTIF)
async def notif_handler(message: Message):
    pass
