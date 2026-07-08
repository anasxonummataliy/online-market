from typing import Optional
from aiogram.types import Message
from database.models import User
from bot.config import conf


async def register_user(msg: Message, parent_id: Optional[int] = None) -> User:
    user = await User.get_user(tg_id=msg.from_user.id)

    if not user:
        admin_id = int(conf.bot.ADMIN) if conf.bot.ADMIN else None
        is_admin = admin_id is not None and msg.from_user.id == admin_id
        user = await User.create(
            tg_id=msg.from_user.id,
            fullname=msg.from_user.full_name,
            username=msg.from_user.username,
            parent_user_id=parent_id,
            type=User.Type.ADMIN if is_admin else User.Type.USER,
        )
    else:
        # Agar DB da USER bo'lsa, lekin ADMIN ID ga mos kelsa — adminlikka o'tkazamiz
        admin_id = int(conf.bot.ADMIN) if conf.bot.ADMIN else None
        if admin_id and msg.from_user.id == admin_id and not user.is_admin:
            await User.update(tg_id=msg.from_user.id, type=User.Type.ADMIN)
            user = await User.get_user(tg_id=msg.from_user.id)

    return user
