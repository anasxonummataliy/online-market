from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import BigInteger
from db import User
from db.base import BaseModel, CreatedBaseModel
from sqlalchemy_file import ImageField


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String)
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(
        ImageField(thumbnail_size=(128, 128)), nullable=True
    )
    quantity: Mapped[int] = mapped_column(BigInteger)
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Category.id), ondelete="CASCADE"
    )


class Card(BaseModel):
    user: Mapped["User"] = relationship("User", back_populates="cards")
