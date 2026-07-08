from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.filters.admin import IsAdmin
from database.models import Category, Product
from bot.states import ProductState
from bot.handlers.private.admin.menu import admin_main_markup


admin_product = Router()
admin_product.message.filter(IsAdmin())
admin_product.callback_query.filter(IsAdmin())


@admin_product.message(F.text == __("Show products 📂"))
async def all_product(message: Message):
    products = await Product.get_all()
    if not products:
        await message.answer(_("No products available."))
        return
    text = _("All Products:\n")
    for product in products:
        text += f"• {product.name} — {product.price} USD\n"
    await message.answer(text)


@admin_product.message(F.text == __("Add product 📂"))
async def add_product(message: Message, state: FSMContext):
    await state.set_state(ProductState.name)
    await message.answer(_("Enter product name."), reply_markup=ReplyKeyboardRemove())


@admin_product.message(ProductState.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ProductState.description)
    await message.answer(_("Enter product description."))


@admin_product.message(ProductState.description)
async def add_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ProductState.price)
    await message.answer(_("Enter product price."))


@admin_product.message(ProductState.price)
async def add_product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer(_("Price must be a number. Please enter again."))
        return
    await state.update_data(price=price)
    await state.set_state(ProductState.quantity)
    await message.answer(_("Enter product quantity."))


@admin_product.message(ProductState.quantity)
async def add_product_quantity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(_("Quantity must be a number. Please enter again."))
        return
    await state.update_data(quantity=int(message.text))
    await state.set_state(ProductState.image)
    await message.answer(_("Send product image (or type /skip to skip)."))


@admin_product.message(ProductState.image, F.text == "/skip")
async def skip_product_image(message: Message, state: FSMContext):
    await state.update_data(file_id=None)
    await _ask_category(message, state)


@admin_product.message(ProductState.image, F.photo)
async def add_product_image(message: Message, state: FSMContext):
    await state.update_data(file_id=message.photo[-1].file_id)
    await _ask_category(message, state)


async def _ask_category(message: Message, state: FSMContext):
    categories = await Category.get_all()
    if not categories:
        await message.answer(_("No categories available. Please add a category first."))
        await state.clear()
        await message.answer(_("Admin menu"), reply_markup=admin_main_markup())
        return
    ikb = InlineKeyboardBuilder()
    for category in categories:
        ikb.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"add_category_{category.id}"
        ))
    ikb.adjust(2)
    await message.answer(_("Select category:"), reply_markup=ikb.as_markup())
    await state.set_state(ProductState.category_id)


@admin_product.callback_query(ProductState.category_id, F.data.startswith("add_category_"))
async def add_product_category_id(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.removeprefix("add_category_"))
    data = await state.get_data()
    await state.clear()

    await Product.create(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        quantity=data["quantity"],
        image=data.get("file_id"),
        category_id=category_id,
    )
    await callback.answer(_("Product added successfully. ✅"), show_alert=True)
    await callback.message.delete()
    await callback.message.answer(_("Admin menu"), reply_markup=admin_main_markup())
