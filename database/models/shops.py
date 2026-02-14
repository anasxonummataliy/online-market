from sqlalchemy_file import ImageField
from sqlalchemy.types import BigInteger
from sqlalchemy import Float, String, select
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload


from .users import User
from database import db, BaseModel, TimeBasedModel


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )


class Product(TimeBasedModel):
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(
        ImageField(thumbnail_size=(128, 128)), nullable=True
    )
    quantity: Mapped[int] = mapped_column(BigInteger)
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("categories.id", ondelete="CASCADE")
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="product"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product"
    )


class Cart(BaseModel):
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="carts")
    cart_item: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="cart"
    )


class CartItem(BaseModel):
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE")
    )
    quantity: Mapped[int] = mapped_column(BigInteger)
    cart_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("carts.id", ondelete="CASCADE")
    )

    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_item")

 
