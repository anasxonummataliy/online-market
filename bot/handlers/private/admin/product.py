from sqlalchemy_file import File
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.filter.admin import IsAdmin
from database.models import Category, Product
from bot.handlers.private import start_handler
from bot.state import CategoryState, ProductState, ChangeCategoryState


admin_product = Router()
admin_product.message.filter(IsAdmin())


@admin_product.message(F.text == "Add category")
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryState.name)
    rkm = ReplyKeyboardRemove()
    await message.answer("Enter category name.", reply_markup=rkm)


@admin_product.message(CategoryState.name)
async def add_category_name(message: Message, state: FSMContext):
    category_name = message.text
    await Category.create(name=category_name)
    await state.clear()
    await message.answer("Category added successfully.")
    await start_handler(message)


@admin_product.message(F.text == "Show categories")
async def all_category(message: Message):
    
    categories = await Category.get_all()
    if not categories:
        await message.answer("No categories available.")
        return
    ikb = InlineKeyboardBuilder()
    for category in categories:
        ikb.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"choice_category_{category.id}"
            )
        )
    ikb.adjust(2)
    await message.answer(
        "Select category to change name:", reply_markup=ikb.as_markup()
    )


@admin_product.callback_query(F.data.startswith("choice_category_"))
async def change_category_name(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.removeprefix("choice_category_"))
    await state.update_data(category_id=category_id)
    rkm = InlineKeyboardBuilder()
    rkm.add(
        InlineKeyboardButton(
            text="Rename ✍️", callback_data=f"rename_category_{category_id}"
        )
    )
    rkm.add(
        InlineKeyboardButton(
            text="Delete 🛒", callback_data=f"delete_category_{category_id}"
        )
    )
    await callback.message.answer(
        f"Which you want delete or rename?", reply_markup=rkm.as_markup()
    )
    await callback.message.delete()


@admin_product.callback_query(F.data.startswith("delete_category_"))
async def delete_category(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.removeprefix("delete_category_")


@admin_product.callback_query(F.data.startswith("rename_category_"))
async def name_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Enter new category name.")
    await state.set_state(ChangeCategoryState.name)


@admin_product.message(ChangeCategoryState.name)
async def change_name_category(message: Message, state: FSMContext):
    category_name = message.text
    data = await state.get_data()
    category_id = data.pop("category_id")
    await Category.update(_id=category_id, name=category_name)
    await state.clear()
    rm = ReplyKeyboardRemove()
    await message.answer("Category name changed successfully.", reply_markup=rm)
    await start_handler(message)


@admin_product.message(F.text == "Show products")
async def all_product(message: Message):
    products = await Product.get_all()
    if not products:
        await message.answer("No products available.")
        return
    text = "All Products:\n"
    for product in products:
        text += f"• {product.name}\n"
    await message.answer(text)


@admin_product.message(F.text == "Add product")
async def add_product(message: Message, state: FSMContext):
    await state.set_state(ProductState.name)
    rkm = ReplyKeyboardRemove()
    await message.answer("Enter product name.", reply_markup=rkm)


@admin_product.message(ProductState.name)
async def add_product_name(message: Message, state: FSMContext):
    product_name = message.text
    await state.update_data(name=product_name)
    await state.set_state(ProductState.description)
    await message.answer("Enter product description.")


@admin_product.message(ProductState.description)
async def add_product_description(message: Message, state: FSMContext):
    product_description = message.text
    await state.update_data(description=product_description)
    await state.set_state(ProductState.price)
    await message.answer("Enter product price.")


@admin_product.message(ProductState.price)
async def add_product_price(message: Message, state: FSMContext):
    product_price = message.text
    if not product_price.isdigit():
        await message.answer("Price must be a number. Please enter again.")
        return
    await state.update_data(price=int(product_price))
    await state.set_state(ProductState.quantity)
    await message.answer("Enter product quantity.")


@admin_product.message(ProductState.quantity)
async def add_product_quantity(message: Message, state: FSMContext):
    product_quantity = message.text
    if not product_quantity.isdigit():
        await message.answer("Quantity must be a number. Please enter again.")
        return
    await state.update_data(quantity=int(product_quantity))
    await state.set_state(ProductState.image)
    await message.answer("Send product image.")


@admin_product.message(ProductState.image, F.photo)
async def add_product_image(message: Message, bot: Bot, state: FSMContext):
    file = message.photo[-1]
    await state.update_data(file_id=file.file_id)

    categories = await Category.get_all()
    ikb = InlineKeyboardBuilder()
    if not categories:
        await message.answer("No categories available. Please add a category first.")
        await state.clear()
        return
    for category in categories:
        ikb.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"add_category_{category.id}"
            )
        )
    ikb.adjust(2)
    await message.answer("Select category:", reply_markup=ikb.as_markup())
    await state.set_state(ProductState.category_id)


@admin_product.callback_query(F.data.startswith("add_category_"))
async def add_product_category_id(callback: CallbackQuery, bot: Bot, state: FSMContext):
    category_id = int(callback.data.removeprefix("add_category_"))
    if not category_id:
        await callback.answer("Category ID must be a number. Please enter again.")
        return
    await state.update_data(category_id=category_id)
    data = await state.get_data()

    file_info = await bot.get_file(data["file_id"])
    file_obj = await bot.download_file(file_info.file_path)
    file = File(file_obj.read(), content_type="image/jpeg")

    await state.clear()
    await Product.create(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        quantity=data["quantity"],
        image=file,
        category_id=data["category_id"],
    )
    await callback.answer("Product added successfully.", show_alert=True)
    await start_handler(callback.message)
    await callback.message.delete()
