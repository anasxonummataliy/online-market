from typing import Optional
from aiogram import Router
from aiogram.types import KeyboardButton, Message, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
    InlineKeyboardButton,
)
from aiogram.utils.i18n import gettext as _

from bot.utils import register_user
from database import User
from bot.buttons.sub_menu import (
    CATEGORIES,
    MY_CART,
    MY_REFERRALS,
    HELP,
    SETTINGS,
    WELCOME_TEXT,
    ADMIN,
)

menu_router = Router()


@menu_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_with_deeplink(msg: Message, command: Command):
    data: str = command.args
    if "_" in data:
        product_id = data.removeprefix("product_")
        user: User = await register_user(msg)
        await User.add_cart(user.tg_id, int(product_id))
        await msg.answer(_("Added to Cart 🛒"))
    else:
        if data.isdigit():
            await start_handler(msg, int(data))

        else:
            await start_handler(msg)


@menu_router.message(CommandStart())
async def start_handler(msg: Message, parent_id: Optional[int] = None):
    await register_user(msg, parent_id)
    ikm = InlineKeyboardBuilder()
    ikm.row(
        InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
        InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="lang_uz"),
    )
    await msg.answer(_(WELCOME_TEXT))
    await msg.answer("Select language / Tilni tanlang", reply_markup=ikm.as_markup())

@menu_router.callback_query(F.data.startswith("lang_"))
async def select_language(callback):
    lang = callback.data.split("_")[1]
    locale
    await callback.message.answer(f"Language set to {lang}")
    await callback.answer()

@menu_router.message(CommandStart())
async def start_handler(msg: Message, parent_id: Optional[int] = None):
    user: User = await register_user(msg, parent_id)
    markup = [
        [KeyboardButton(text=_(CATEGORIES))],
        [KeyboardButton(text=_(HELP)), KeyboardButton(text=_(MY_REFERRALS))],
        [KeyboardButton(text=_(SETTINGS)), KeyboardButton(text=_(MY_CART))],
    ]
    if user.is_admin:
        markup.append([KeyboardButton(text=ADMIN)])
    rkb = ReplyKeyboardBuilder(markup=markup)
    await msg.answer(_(WELCOME_TEXT), reply_markup=rkb.as_markup())
