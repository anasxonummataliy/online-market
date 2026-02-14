from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import CartItem, User

cart_router = Router()


@cart_router.message(F.text == "My carts 🛒")
async def cart_handler(message: Message):
    cart_items = await CartItem.get_by_user_id(message.from_user.id)

    if cart_items:
        ikm = InlineKeyboardBuilder()
        for cart in cart_items:
            ikm.row(
                InlineKeyboardButton(text="＋", callback_data="product_add_to_cart_"),
                InlineKeyboardButton(text=cart.product.name, callback_data="123"),
                InlineKeyboardButton(
                    text="−", callback_data="product_remove_from_cart_"
                ),
            )


@cart_router.callback_query(F.data == "product_remove_from_cart_")
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.removeprefix("product_remove_from_cart_"))
    has_deleted = await User.remove_cart(callback.message.from_user.id, product_id)

    if has_deleted:
        await callback.message.delete()
        await callback.answer("Remove from Cart", show_alert=True)

    else:
        await callback.answer("No cart items!", show_alert=True)
