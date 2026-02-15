from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Enum as SqlEnum, ForeignKey, select

from database.base import db, TimeBasedModel
if TYPE_CHECKING:
    from database.models import Cart, Order


class User(TimeBasedModel):
    class Type(Enum):
        ADMIN = "admin"
        USER = "user"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    type: Mapped[SqlEnum] = mapped_column(SqlEnum(Type), default=Type.USER)
    parent_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

    @property
    def is_admin(self) -> bool:
        return self.type == self.Type.ADMIN

    @classmethod
    async def get_user(cls, tg_id: int):
        return (await db.execute(select(cls).where(cls.tg_id == tg_id))).scalar()

    @classmethod
    async def add_cart(cls, tg_id: int, product_id: int, quantity: int = 1):
        user = await User.get_user(tg_id=tg_id)

        from .shops import Cart

        cart = await Cart.filter_one(user_id=user.id)
        if cart is None:
            cart = await Cart.create(user_id=user.id)
        from database.models import CartItem

        cart_item = await CartItem.filter_one(cart_id=cart.id, product_id=product_id)

        if cart_item is not None:
            cart_item.quantity += quantity
            await cart_item.save_model()
        else:
            await CartItem.create(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )

    @classmethod
    async def remove_cart(cls, tg_id: int, product_id: int):
        user = await cls.filter_one(tg_id=tg_id)
        if not user:
            return False

        from .shops import Cart, CartItem

        cart = await Cart.filter_one(user_id=user.id)
        if not cart:
            return False

        cart_item = await CartItem.filter_one(cart_id=cart.id, product_id=product_id)

        if not cart_item:
            return False

        if cart_item.quantity > 1:
            await CartItem.update(_id=cart_item.id, quantity=cart_item.quantity - 1)
        else:
            await CartItem.delete(_id=cart_item.id)

        return True

    @classmethod
    async def clear_cart(cls, tg_id: int):
        user = await User.filter_one(tg_id=tg_id)
        from .shops import Cart

        cart = await Cart.filter_one(user_id=user.id)
        if cart is None:
            return False

        from .shops import CartItem

        cart_items = await CartItem.filter(cart_id=cart.id)
        for item in cart_items:
            await CartItem.delete(_id=item.id)

        await Cart.delete(_id=cart.id)
        return True
