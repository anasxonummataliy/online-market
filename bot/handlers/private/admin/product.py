from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.filter.admin import IsAdmin
from database.models import Category, Product
from bot.handlers.private import start_handler
from bot.state import AdminState, CategoryState, ProductState


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


@admin_product.message(F.text == "All category")
async def all_category(message: Message):
    categories = await Category.all()
    if not categories:
        await message.answer("No categories available.")
        return
    text = "All Categories:\n"
    for category in categories:
        text += f"• {category.name}\n"
    await message.answer(text)


@admin_product.message(F.text == "All product")
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
async def add_product_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = f"media/products/{photo.file_unique_id}.jpg"
    await message.bot.download_file(file.file_path, destination=file_path)
    await state.update_data(image=file_path)
    await state.set_state(ProductState.category_id)

    await message.answer("Enter category ID for the product.")


@admin_product.message(ProductState.category_id)
async def add_product_category_id(message: Message, state: FSMContext):
    category_id = message.text
    if not category_id.isdigit():
        await message.answer("Category ID must be a number. Please enter again.")
        return
    await state.update_data(category_id=int(category_id))
    data = await state.get_data()
    await Product.create(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        quantity=data["quantity"],
        image=data["image"],
        category_id=data["category_id"],
    )
    await state.clear()
    await message.answer("Product added successfully.")
    await start_handler(message)
