from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import CartItem

cart_router = Router()


@cart_router.message(F.text == "My carts 🛒")
async def cart_handler(message: Message):
    cart_items = await CartItem.get_by_user_id(message.from_user.id)

    if cart_item:
        ikm = InlineKeyboardBuilder()
        for cart_item in cart_items:
            ikm.row(InlineKeyboardButton(text="＋"))
