from enum import Enum
from sqlalchemy import BigInteger, Integer, Enum as SQLEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from database import TimeBasedModel


class Order(TimeBasedModel):
    class Status(Enum):
        IN_PROGRESS = "jarayonda"
        PAID = "to'langan"
        CANCELLED = "bekor qilingan"

    user: Mapped["User"] = relationship("User", back_populates="orders")
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categories.id", ondelete="CASCADE"),
    )

    status: Mapped[SQLEnum] = mapped_column(SQLEnum(Status), default=Status.IN_PROGRESS)
    order_items: Mapped[list["OrderItem"]] = relationship(
        "order_items.id", back_populates="order"
    )


class OrderItem(TimeBasedModel):
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('orders.id', ondelete="CASCADE")
    )
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE")
    )

    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
