from aiogram import Bot, Router, F
from aiogram.types import Message
from bot.buttons.sub_menu import MY_REFERRALS, HELP

referrals_router = Router()

@referrals_router.message(F.text == MY_REFERRALS)
async def my_referrals():
    pass
