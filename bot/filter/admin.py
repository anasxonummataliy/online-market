from aiogram.filters import Filter

from database import User

class IsAdmin(Filter):
    async def __call__(self, message):
        user = await User.get_user(tg_id=message.from_user.id)
        return user.is_admin


