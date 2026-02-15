from typing import Optional
from aiogram import Router, Bot
from aiogram.types import KeyboardButton, Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils import register_user
from database import User
from bot.buttons.sub_menu import (
    CATEGORIES,
    MY_REFERRALS,
    HELP,
    SETTINGS,
    WELCOME_TEXT,
    ADMIN,
)

menu_router = Router()


@menu_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_with_deeplink(msg: Message, command: Command):
    data = command.args
    if "_" in data:
        product_id = data.removeprefix("product_")
        user = await register_user(msg)
        await User.add_cart(user.tg_id, int(product_id))
        await msg.answer("Added to Cart 🛒")
    else:
        if data.isdigit():
            await start_handler(msg, int(data))

        else:
            await start_handler(msg)


@menu_router.message(CommandStart())
async def start_handler(msg: Message, parent_id: Optional[int] = None):
    user = await register_user(msg, parent_id)

    markup = [
        [KeyboardButton(text=CATEGORIES)],
        [KeyboardButton(text=HELP), KeyboardButton(text=MY_REFERRALS)],
        [KeyboardButton(text=SETTINGS), KeyboardButton(text="My carts 🛒")],
    ]
    if user.is_admin:
        markup.append([KeyboardButton(text=ADMIN)])
    rkb = ReplyKeyboardBuilder(markup=markup)
    await msg.answer((WELCOME_TEXT), reply_markup=rkb.as_markup())
