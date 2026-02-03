from aiogram import Router, Bot
from aiogram.types import KeyboardButton, Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons.sub_menu import MY_REFERRALS, HELP
from database import User
from database.base import db

menu_router = Router()

@menu_router.message(CommandStart())
async def start_handler(msg: Message):
    # user_data = {
    #     "telegram_id": msg.from_user.id,
    #     "fullname": msg.from_user.full_name,
    #     "username": msg.from_user.username,
    # }
    # await User.create(**user_data)
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text='Help'), KeyboardButton(text=MY_REFERRALS)])
    await msg.answer("Salom", reply_markup=rkb.as_markup())
