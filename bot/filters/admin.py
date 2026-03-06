from aiogram.filters import Filter
from aiogram.types import Message

from database import User


class IsAdmin(Filter):
    async def __call__(self, message: Message):
        user = await User.get_user(tg_id=message.from_user.id)
        return user.is_admin
