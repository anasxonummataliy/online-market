from enum import Enum
from sqlalchemy import BigInteger, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey


from db.base import TimeBasedModel
from db import User


class Order(TimeBasedModel):
    class Status(Enum):
        IN_PROGRESS = "jarayonda"
        PAID = "to'langan"
        CANCELLED = "bekor qilingan"

    user: Mapped["User"] = relationship("User", back_populates="orders")
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.id), ondelete="CASCADE"
    )
    status: Mapped[SQLEnum] = mapped_column(SQLEnum(Status), default=Status.IN_PROGRESS)
    
