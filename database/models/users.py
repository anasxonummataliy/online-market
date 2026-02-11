from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Enum as SqlEnum, ForeignKey, select

from database import *



class User(TimeBasedModel):
    __tablename__ = "users"

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
    async def add_cart(cls, user_id, product_id, quantity: int = 1):
        cart = await Cart.create(user_id=user_id)
        cart_item = await CartItem.create(
            cart_id=cart.id, product_id=product_id, quantity=quantity
        )

    @classmethod
    async def remove_cart(cls, user_id: int, product_id: int):
        cart_item = await CartItem.delete_by_user_product(
            user_id=user_id, product_id=product_id
        )
