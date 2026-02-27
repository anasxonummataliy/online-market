from typing import Optional
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, get_i18n
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


@menu_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_with_deeplink(msg: Message, command: CommandObject):
    data: str = command.args
    print(type(command))
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
async def start_handler(
    msg: Message, parent_id: Optional[int] = None, state: FSMContext = None
):
    await register_user(msg, parent_id)
    print("User registered")
    user: User = await User.get_user(tg_id=msg.from_user.id)
    if not user.locale:
        await language_handler(msg)
        return
    get_i18n().current_locale = user.locale
    if state:
        await state.update_data(locale=user.locale)
    await msg.answer(_(WELCOME_TEXT))


@menu_router.message(F.text == str(CHANGE_LANG))
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
    markup = [
        [KeyboardButton(text=str(CATEGORIES))],
        [KeyboardButton(text=str(HELP)), KeyboardButton(text=str(MY_REFERRALS))],
        [KeyboardButton(text=str(SETTINGS)), KeyboardButton(text=str(MY_CART))],
    ]
    if user.is_admin:
        markup.append([KeyboardButton(text=str(ADMIN))])
    rkb = ReplyKeyboardBuilder(markup=markup)
    await state.update_data(locale=lang)
    get_i18n().current_locale = lang
    await callback.message.answer(
        _(WELCOME_TEXT, locale=lang),
        reply_markup=rkb.as_markup(),
    )
    await callback.answer()
