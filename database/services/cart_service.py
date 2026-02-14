from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models.users import User
from database.models.shops import Cart
from database.base import db


class CartService:
    @classmethod
    async def get_by_user_id(cls, tg_id: int):
        user = await User.filter_one(tg_id=tg_id)
        query = (
            select(User)
            .join(Cart)
            .options(selectinload(cls.product), selectinload(cls.cart))
            .where(Cart.user_id == user.id)
        )
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_by_user_id(cls, user_id: int):
        query = (
            select(User)
            .join(Cart)
            .options(selectinload(cls.product), selectinload(cls.cart))
            .where(Cart.user_id == user_id)
        )
        return (await db.execute(query)).scalars().all()
