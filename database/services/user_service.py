from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import Cart, CartItem, db


class UserService:
    @property
    def is_admin(self) -> bool:
        return self.type == self.Type.ADMIN

    @classmethod
    async def get_user(cls, tg_id: int):
        return (await db.execute(select(cls).where(cls.tg_id == tg_id))).scalar()

    @classmethod
    async def add_cart(cls, tg_id: int, product_id: int, quantity: int = 1):
        user = await cls.filter_one(tg_id=tg_id)
        cart = await Cart.filter_one(user_id=user.id)
        if cart is None:
            cart = await Cart.create(user_id=user.id)

        cart_item = await CartItem.filter_one(cart_id=cart.id, product_id=product_id)

        if cart_item is not None:
            cart_item.quantity += quantity
            await cart_item.save_model()
        else:
            await CartItem.create(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )

    @classmethod
    async def remove_cart(cls, user_id: int, product_id: int):
        cart = await Cart.filter(user_id=user_id).first()
        if cart is None:
            return False

        query = select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == product_id
        )
        cart_item = (await db.execute(query)).scalar_one_or_none()

        if not cart_item:
            return False

        if cart_item.quantity < 2:
            await db.delete(cart_item)

        else:
            cart_item.quantity -= 1
            db.add(cart_item)

        await CartItem.commit()
        return True
