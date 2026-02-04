from typing import Optional
from aiogram import Router, Bot
from aiogram.types import KeyboardButton, Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons.sub_menu import CATEGORIES, MY_REFERRALS, HELP, SETTINGS, WELCOME_TEXT
from database import User
from database.base import db

menu_router = Router()


@menu_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_with_deeplink(msg: Message, command: Command):
    user_id = command.args
    if user_id.isdigit():
        await start_handler(msg, int(user_id))

    else:
        await start_handler(msg)


@menu_router.message(CommandStart())
async def start_handler(msg: Message, parent_id: Optional[int] = None):
    await User.create(
        id=msg.from_user.id,
        fullname=msg.from_user.full_name,
        username=msg.from_user.username,
        parent_user_id=parent_id,
    )
    markup = [
        [KeyboardButton(text=CATEGORIES)],
        [KeyboardButton(text=HELP), KeyboardButton(text=MY_REFERRALS)],
        [KeyboardButton(text=SETTINGS)]
    ]
    rkb = ReplyKeyboardBuilder(markup=markup)
    await msg.answer((WELCOME_TEXT), reply_markup=rkb.as_markup())
