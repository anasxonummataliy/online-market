from aiogram import Router
from aiogram.types import Message

from bot.config import conf
from bot.filter.admin import IsAdmin

admin_product = Router()
admin_product.message.filter(IsAdmin())

@admin_product.message()
async def product(message: Message):
    pass
