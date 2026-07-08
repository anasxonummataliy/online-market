from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database import User


class IsAdmin(Filter):
    async def __call__(self, update: Message | CallbackQuery):
        tg_id = update.from_user.id
        user = await User.get_user(tg_id=tg_id)
        if user is None:
            return False
        return user.is_admin
