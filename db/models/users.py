from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel
from db import Card


class User(BaseModel):
    fullname: Mapped[str] = mapped_column(String)
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="user")
