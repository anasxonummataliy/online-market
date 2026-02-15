from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import CartItem, User

cart_router = Router()


async def build_cart_message(tg_id: int):
    cart_items = await CartItem.get_by_user_id(tg_id)

    if not cart_items:
        return "Savatingiz bo'sh ❌", None

    text = "🛒 Savatingiz:\n\n"
    total = 0
    ikm = InlineKeyboardBuilder()

    for cart_item in cart_items:
        item_total = cart_item.product.price * cart_item.quantity
        text += f"📦 {cart_item.product.name}\n"
        text += f"   💰 {cart_item.product.price} ＄ x {cart_item.quantity}\n"
        text += f"   💵 {item_total} ＄\n\n"
        total += item_total

        ikm.row(
            InlineKeyboardButton(
                text="➕",
                callback_data=f"cart_add_{cart_item.product_id}",
                style="success",
            ),
            InlineKeyboardButton(
                text=f"{cart_item.product.name} ({cart_item.quantity})",
                callback_data="ignore",
                style="primary",
            ),
            InlineKeyboardButton(
                text="➖",
                callback_data=f"cart_remove_{cart_item.product_id}",
                style="danger",
            ),
        )

    text += f"\n💰 All: {total} ＄"

    ikm.row(InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="cart_clear"))

    ikm.row(
        InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="cart_checkout")
    )

    return text, ikm.as_markup()


@cart_router.message(F.text == "My carts 🛒")
async def cart_handler(message: Message):

    text, markup = await build_cart_message(message.from_user.id)
    await message.answer(text, reply_markup=markup)


@cart_router.callback_query(F.data.startswith("cart_add_"))
async def cart_add_quantity(callback: CallbackQuery):

    product_id = int(callback.data.removeprefix("cart_add_"))

    try:
        await User.add_cart(callback.from_user.id, product_id)
        await callback.answer("✅ +1", show_alert=False)

        text, markup = await build_cart_message(callback.from_user.id)
        await callback.message.edit_text(text, reply_markup=markup)

    except Exception as e:
        await callback.answer(f"❌ Xato: {e}", show_alert=True)


@cart_router.callback_query(F.data.startswith("cart_remove_"))
async def cart_remove_quantity(callback: CallbackQuery):

    product_id = int(callback.data.removeprefix("cart_remove_"))

    try:
        success = await User.remove_cart(callback.from_user.id, product_id)

        if success:
            await callback.answer("✅ -1", show_alert=False)

            text, markup = await build_cart_message(callback.from_user.id)

            if markup:
                await callback.message.edit_text(text, reply_markup=markup)
            else:
                await callback.message.edit_text(text)
        else:
            await callback.answer("❌ Mahsulot topilmadi", show_alert=True)

    except Exception as e:
        await callback.answer(f"❌ Xato: {e}", show_alert=True)


@cart_router.callback_query(F.data == "cart_clear")
async def cart_clear_handler(callback: CallbackQuery):

    success = await User.clear_cart(callback.from_user.id)

    if success:
        await callback.message.edit_text("Savatingiz bo'sh ❌")
        await callback.answer("🗑 Savat tozalandi", show_alert=True)
    else:
        await callback.answer("❌ Savat topilmadi", show_alert=True)
