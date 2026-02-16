from aiogram import Router, Bot, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, FSInputFile, Message, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.buttons.sub_menu import *
from database.models import Category, Product, User

product_router = Router()


@product_router.message(F.text == CATEGORIES)
async def get_all_categories(message: Message):
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories != []:
        for category in categories:
            ikm.add(
                InlineKeyboardButton(
                    text=category.name,
                    callback_data=f"category_{category.id}",
                )
            )
        ikm.adjust(2)
        await message.answer("Categories", reply_markup=ikm.as_markup())
    else:
        await message.answer("No categories")


def make_product(product, category_id):
    ikm = InlineKeyboardBuilder()
    ikm.row(
        InlineKeyboardButton(
            text=f"{product.name} {product.price} 💵",
            callback_data=f"product_{product.id}",
        )
    )
    ikm.row(
        InlineKeyboardButton(
            text=_("⏮️ Previous"),
            callback_data=f"product_previous_{product.id}_{category_id}",
        ),
        InlineKeyboardButton(
            text=_("Add to Cart 🛒"),
            callback_data=f"product_add_to_cart_{product.id}",
        ),
        InlineKeyboardButton(
            text=_("Next ⏭️"), callback_data=f"product_next_{product.id}_{category_id}"
        ),
    )
    ikm.row(InlineKeyboardButton(text="⏮️ Back", callback_data="back_to_categotry"))
    caption = _(
        "<b>Name:</b> {name}\n"
        "<b>Description:</b> {description}\n"
        "<b>Price:</b> {price} USD\n"
        "<b>Quantity:</b> {quantity}"
    ).format(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )

    return (
        caption,
        ikm.as_markup(),
    )


async def send_product(callback, product, category_id):
    caption, ikm = make_product(product, category_id)

    try:
        await callback.message.delete()
    except:
        pass

    if product.image:
        await callback.message.answer_photo(
            photo=FSInputFile(product.image["url"]),
            caption=caption,
            reply_markup=ikm,
            parse_mode=ParseMode.HTML,
        )
    else:
        await callback.message.answer(
            caption,
            reply_markup=ikm,
            parse_mode=ParseMode.HTML,
        )


@product_router.callback_query(F.data.startswith("category_"))
async def callback_categories(callback: CallbackQuery):
    category_id = callback.data.removeprefix("category_")
    product = await Product.filter_for_category(int(category_id))

    if product:
        await callback.message.delete()
        caption, ikm = make_product(product, category_id)
        if product.image:
            await callback.message.answer_photo(
                photo=FSInputFile(product.image["url"]),
                caption=caption,
                reply_markup=ikm.as_markup(),
                parse_mode=ParseMode.HTML,
            )
        else:
            await callback.message.answer(
                text=caption, reply_markup=ikm, parse_mode=ParseMode.HTML
            )
    else:
        await callback.answer(_("No product"), show_alert=True)


@product_router.callback_query(F.data.startswith("product_next_"))
async def get_next_product(callback: CallbackQuery):
    product_id, category_id = map(
        int, callback.data.removeprefix("product_next_").split("_")
    )
    product = await Product.get_next_product_by_category(category_id, product_id)
    if not product:
        await callback.answer(_("Last product"), show_alert=True)
        return

    caption, ikm = make_product(product, category_id)
    await send_product(callback, product, category_id)


@product_router.callback_query(F.data.startswith("product_previous_"))
async def get_previous_product(callback: CallbackQuery):
    product_id, category_id = map(
        int, callback.data.removeprefix("product_previous_").split("_")
    )
    product = await Product.get_previous_product_by_category(category_id, product_id)
    if not product:
        await callback.answer(_("First product"), show_alert=True)
        return
    await send_product(callback, product, category_id)


@product_router.callback_query(F.data.startswith("back_to_categotry"))
async def back_to_category(callback: CallbackQuery):
    await callback.message.delete()
    await get_all_categories(callback.message)


@product_router.callback_query(F.data.startswith("product_add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = callback.data.removeprefix("product_add_to_cart_")
    await User.add_cart(callback.from_user.id, int(product_id))
    await callback.answer(_("Added to Cart 🛒"), show_alert=True)
