from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.filters.admin import IsAdmin
from database.models import Category
from bot.states import CategoryState, ChangeCategoryState
from bot.handlers.private.admin.menu import admin_main_markup


admin_category = Router()
admin_category.message.filter(IsAdmin())
admin_category.callback_query.filter(IsAdmin())


@admin_category.message(F.text == __("Add category 📂"))
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryState.name)
    await message.answer(_("Enter category name."), reply_markup=ReplyKeyboardRemove())


@admin_category.message(CategoryState.name)
async def add_category_name(message: Message, state: FSMContext):
    await Category.create(name=message.text)
    await state.clear()
    await message.answer(_("Category added successfully. ✅"), reply_markup=admin_main_markup())


@admin_category.message(F.text == __("Show categories 📂"))
async def all_category(message: Message):
    categories = await Category.get_all()
    if not categories:
        await message.answer(_("No categories available."))
        return
    ikb = InlineKeyboardBuilder()
    for category in categories:
        ikb.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"choice_category_{category.id}"
        ))
    ikb.adjust(2)
    await message.answer(_("Select category:"), reply_markup=ikb.as_markup())


@admin_category.callback_query(F.data.startswith("choice_category_"))
async def choice_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.removeprefix("choice_category_"))
    await state.update_data(category_id=category_id)
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_("Rename ✍️"), callback_data=f"rename_category_{category_id}"))
    ikb.add(InlineKeyboardButton(text=_("Delete 🗑"), callback_data=f"delete_category_{category_id}"))
    await callback.message.answer(_("What do you want to do?"), reply_markup=ikb.as_markup())


@admin_category.callback_query(F.data.startswith("delete_category_"))
async def delete_category(callback: CallbackQuery):
    category_id = int(callback.data.removeprefix("delete_category_"))
    await Category.delete(_id=category_id)
    await callback.message.delete()
    await callback.message.answer(_("Category deleted. ✅"), reply_markup=admin_main_markup())


@admin_category.callback_query(F.data.startswith("rename_category_"))
async def rename_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    msg = await callback.message.answer(_("Enter new category name."))
    await state.update_data(rename_msg_id=msg.message_id)
    await state.set_state(ChangeCategoryState.name)


@admin_category.message(ChangeCategoryState.name)
async def save_renamed_category(message: Message, state: FSMContext):
    data = await state.get_data()
    rename_msg_id = data.get("rename_msg_id")
    category_id = data.get("category_id")

    if rename_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=rename_msg_id)
        except Exception:
            pass

    await Category.update(_id=category_id, name=message.text)
    await state.clear()
    await message.answer(_("Category renamed. ✅"), reply_markup=admin_main_markup())
