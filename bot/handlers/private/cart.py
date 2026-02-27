from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.buttons.sub_menu import MY_CART
from database import CartItem, User

cart_router = Router()


async def build_cart_message(tg_id: int):
    cart_items = await CartItem.get_by_user_id(tg_id)

    if not cart_items:
        return _("Your cart is empty ❌"), None

    text = _("🛒 Your cart:\n\n")
    total = 0
    ikm = InlineKeyboardBuilder()

    for cart_item in cart_items:
        item_total = cart_item.product.price * cart_item.quantity
        total += item_total

        text += _(
            "📦 {name}\n" "   💰 {price} ＄ x {quantity}\n" "   💵 {item_total} ＄\n\n"
        ).format(
            name=cart_item.product.name,
            price=cart_item.product.price,
            quantity=cart_item.quantity,
            item_total=item_total,
        )

        ikm.row(
            InlineKeyboardButton(
                text="➕",
                callback_data=f"cart_add_{cart_item.product_id}",
            ),
            InlineKeyboardButton(
                text="{name} ({quantity})".format(
                    name=cart_item.product.name,
                    quantity=cart_item.quantity,
                ),
                callback_data="ignore",
            ),
            InlineKeyboardButton(
                text="➖",
                callback_data=f"cart_remove_{cart_item.product_id}",
            ),
        )

    text += _("\n💰 Total: {total} ＄").format(total=total)

    ikm.row(InlineKeyboardButton(text=_("🗑 Clear cart"), callback_data="cart_clear"))

    ikm.row(InlineKeyboardButton(text=_("✅ Checkout"), callback_data="cart_checkout"))

    return text, ikm.as_markup()


@cart_router.message(F.text == MY_CART)
async def cart_handler(message: Message):
    text, markup = await build_cart_message(message.from_user.id)
    await message.answer(text, reply_markup=markup)


@cart_router.callback_query(F.data.startswith("cart_add_"))
async def cart_add_quantity(callback: CallbackQuery):

    product_id = int(callback.data.removeprefix("cart_add_"))

    try:
        await User.add_cart(callback.from_user.id, product_id)

        await callback.answer(_("✅ Added +1"))

        text, markup = await build_cart_message(callback.from_user.id)
        await callback.message.edit_text(text, reply_markup=markup)

    except Exception as e:
        await callback.answer(_("❌ Error: {error}").format(error=e), show_alert=True)


@cart_router.callback_query(F.data.startswith("cart_remove_"))
async def cart_remove_quantity(callback: CallbackQuery):

    product_id = int(callback.data.removeprefix("cart_remove_"))

    try:
        success = await User.remove_cart(callback.from_user.id, product_id)

        if success:
            await callback.answer(_("✅ Removed -1"))

            text, markup = await build_cart_message(callback.from_user.id)

            if markup:
                await callback.message.edit_text(text, reply_markup=markup)
            else:
                await callback.message.edit_text(text)

        else:
            await callback.answer(_("❌ Product not found"), show_alert=True)

    except Exception as e:
        await callback.answer(_("❌ Error: {error}").format(error=e), show_alert=True)


@cart_router.callback_query(F.data == "cart_clear")
async def cart_clear_handler(callback: CallbackQuery):

    success = await User.clear_cart(callback.from_user.id)

    if success:
        await callback.message.edit_text(_("Your cart is empty ❌"))
        await callback.answer(_("🗑 Cart cleared"), show_alert=True)

    else:
        await callback.answer(_("❌ Cart not found"), show_alert=True)
