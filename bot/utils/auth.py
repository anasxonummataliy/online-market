from typing import Optional
from database.models import User


async def register_user(msg, parent_id: Optional[int] = None):
    if not await User.get_user(tg_id=msg.from_user.id):
        await User.create(
            tg_id=msg.from_user.id,
            fullname=msg.from_user.full_name,
            username=msg.from_user.username,
            parent_user_id=parent_id,
        )

    return await User.get_user(tg_id=msg.from_user.id)
