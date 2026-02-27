from typing import Optional
from aiogram.types import Message
from database.models import User


async def register_user(msg: Message, parent_id: Optional[int] = None) -> User:
    if not await User.get_user(tg_id=msg.from_user.id):
        await User.create(
            tg_id=msg.from_user.id,
            fullname=msg.from_user.full_name,
            username=msg.from_user.username,
            parent_user_id=parent_id,
        )

    return await User.get_user(tg_id=msg.from_user.id)
