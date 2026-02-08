from aiogram import Router, Bot, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, FSInputFile, Message, InlineKeyboardButton

from bot.buttons.sub_menu import *
from database.models.shops import Category, Product

product_router = Router()


@product_router.message(F.text == CATEGORIES)
async def get_all_categories(message: Message):
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories != []:
        for category in categories:
            ikm.add(
                InlineKeyboardButton(
                    text=category.name, callback_data=f"category_{category.id}"
                )
            )
        ikm.adjust(2)
        await message.answer("Categories", reply_markup=ikm.as_markup())
    else:
        await message.answer("No categories")


@product_router.callback_query(F.data.startswith("category_"))
async def callback_categories(callback: CallbackQuery, bot: Bot):
    category_id = callback.data.removeprefix("category_")
    products = await Product.filter_for_category(int(category_id))
    ikm = InlineKeyboardBuilder()
    if len(products):
        product = products[1]
        ikm.row(
            InlineKeyboardButton(
                text=f"{product.name} {product.price} 💵",
                callback_data=f"product_{product.id}",
            )
        )
        ikm.row(
            InlineKeyboardButton(
                text="⏮️ Previous", callback_data=f"product_previous_{product.id}"
            ),
            InlineKeyboardButton(
                text="Add to Cart 🛒",
                callback_data=f"product_add_to_cart_{product.id}",
            ),
            InlineKeyboardButton(
                text="Next ⏭️", callback_data=f"product_next_{product.id}"
            ),
        )
        await callback.message.delete()
        caption = f"""<b>Name</b> {product.name}
<b>Description:</b> {product.description}
<b>Price:</b> {product.price} USD
<b>Quantity:</b> {product.quantity}"""
        if product.image:
            await callback.message.answer_photo(
                photo=FSInputFile(product.image['url']),
                caption=caption,
                reply_markup=ikm.as_markup(),
                parse_mode=ParseMode.HTML,
            )
        else:
            await callback.message.answer(
                text=caption, reply_markup=ikm.as_markup(), parse_mode=ParseMode.HTML
            )
    else:
        await callback.answer("No product", show_alert=True)
