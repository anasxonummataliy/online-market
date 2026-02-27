from typing import Optional
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import get_i18n
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardButton, KeyboardButton, Message
from bot.buttons.sub_menu import (
    ADMIN,
    CATEGORIES,
    CHANGE_LANG,
    HELP,
    MY_CART,
    MY_REFERRALS,
    SETTINGS,
    WELCOME_TEXT,
)
from bot.utils import register_user
from database import User


menu_router = Router()


def build_main_markup(user: User):
    markup = [
        [KeyboardButton(text=str(CATEGORIES))],
        [KeyboardButton(text=str(HELP)), KeyboardButton(text=str(MY_REFERRALS))],
        [KeyboardButton(text=str(SETTINGS)), KeyboardButton(text=str(MY_CART))],
    ]
    if user.is_admin:
        markup.append([KeyboardButton(text=str(ADMIN))])
    return ReplyKeyboardBuilder(markup=markup).as_markup(resize_keyboard=True)


async def send_main_menu(message: Message, user: User, state: FSMContext = None):
    get_i18n().current_locale = user.locale
    if state:
        await state.update_data(locale=user.locale)
    await message.answer(str(WELCOME_TEXT), reply_markup=build_main_markup(user))


@menu_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_with_deeplink(msg: Message, command: CommandObject, state: FSMContext):
    data: str = command.args
    if "_" in data:
        product_id = data.removeprefix("product_")
        user: User = await register_user(msg)
        await User.add_cart(user.tg_id, int(product_id))
        await msg.answer("Added to Cart 🛒")
    else:
        parent_id = int(data) if data.isdigit() else None
        await _start(msg, state, parent_id)


@menu_router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await _start(msg, state)


async def _start(msg: Message, state: FSMContext, parent_id: Optional[int] = None):
    await register_user(msg, parent_id)
    user: User = await User.get_user(tg_id=msg.from_user.id)
    if not user.locale:
        await language_handler(msg)
        return
    await send_main_menu(msg, user, state)


@menu_router.message(F.text == CHANGE_LANG)
async def language_handler(message: Message):
    ikm = InlineKeyboardBuilder()
    ikm.row(
        InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
        InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="lang_uz"),
    )
    await message.answer(
        "Select language / Tilni tanlang", reply_markup=ikm.as_markup()
    )


@menu_router.callback_query(F.data.startswith("lang_"))
async def select_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await User.update(telegram_id=callback.from_user.id, locale=lang)
    user: User = await User.get_user(tg_id=callback.from_user.id)
    await send_main_menu(callback.message, user, state)
    await callback.answer()
