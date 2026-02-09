from aiogram import Router
from aiogram.types import Message

from bot.config import conf

admin_product = Router()

@admin_product.message()
async def product(message: Message):
    pass
