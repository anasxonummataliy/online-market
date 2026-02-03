from enum import Enum
from sqlalchemy import BigInteger, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import TimeBasedModel


class User(TimeBasedModel):
    class Type(Enum):
        ADMIN = "admin"
        USER = "user"

    fullname: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    type: Mapped[SqlEnum] = mapped_column(SqlEnum(Type), default=Type.USER)
    parent_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
