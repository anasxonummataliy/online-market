from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)

from bot.filter.admin import IsAdmin
from database.models import Category
from bot.handlers.private import start_handler
from bot.state import CategoryState, ChangeCategoryState


admin_category = Router()
admin_category.message.filter(IsAdmin())


@admin_category.message(F.text == "Add category")
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryState.name)
    rkm = ReplyKeyboardRemove()
    await message.answer("Enter category name.", reply_markup=rkm)


@admin_category.message(CategoryState.name)
async def add_category_name(message: Message, state: FSMContext):
    category_name = message.text
    await Category.create(name=category_name)
    await state.clear()
    await message.answer("Category added successfully.")
    await start_handler(message)


@admin_category.message(F.text == "Show categories")
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


@admin_category.callback_query(F.data.startswith("choice_category_"))
async def change_category_name(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.removeprefix("choice_category_"))
    await state.update_data(category_id=category_id)
    await callback.message.delete()
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


@admin_category.callback_query(F.data.startswith("delete_category_"))
async def delete_category(callback: CallbackQuery):
    category_id = callback.data.removeprefix("delete_category_")
    await Category.delete(_id=int(category_id))
    await callback.message.delete()
    await callback.message.answer("Category deleted successfully.")
    await start_handler(callback.message)


@admin_category.callback_query(F.data.startswith("rename_category_"))
async def name_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    msg = await callback.message.answer("Enter new category name.")
    await state.update_data(rename_msg_id=msg.message_id)
    await state.set_state(ChangeCategoryState.name)


@admin_category.message(ChangeCategoryState.name)
async def change_name_category(message: Message, state: FSMContext):
    data = await state.get_data()
    rename_msg_id = data.pop("rename_msg_id")
    if rename_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=rename_msg_id
            )
        except Exception:
            pass

    category_name = message.text
    category_id = data.pop("category_id")
    await Category.update(_id=category_id, name=category_name)
    await state.clear()
    rm = ReplyKeyboardRemove()
    await message.answer("Category name changed successfully.", reply_markup=rm)
    await start_handler(message)
