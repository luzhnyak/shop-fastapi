from app.core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cart import CartRepository, CartItemRepository

from app.schemas.cart import (
    CartRead,
    CartItemCreate,
    CartItemRead,
)


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemRepository(db)

    async def get_cart(self, user_id: int) -> CartRead:
        cart = await self.cart_repo.find_one(user_id=user_id)
        if not cart:
            # якщо кошика ще нема — створюємо
            cart = await self.cart_repo.add_one({"user_id": user_id})

        items = await self.cart_item_repo.find_all(cart_id=cart.id)
        cart_dict = CartRead.model_validate(cart).model_dump()
        cart_dict["items"] = [CartItemRead.model_validate(i) for i in items]

        return CartRead(**cart_dict)

    async def add_item(self, user_id: int, item_data: CartItemCreate) -> CartRead:
        cart = await self.cart_repo.find_one(user_id=user_id)
        if not cart:
            cart = await self.cart_repo.add_one({"user_id": user_id})

        # шукаємо чи вже є такий товар у кошику
        existing_item = await self.cart_item_repo.find_one(
            cart_id=cart.id, product_id=item_data.product_id
        )

        if existing_item:
            await self.cart_item_repo.edit_one(
                existing_item.id,
                {"quantity": existing_item.quantity + item_data.quantity},
            )
        else:
            await self.cart_item_repo.add_one(
                {
                    "cart_id": cart.id,
                    "product_id": item_data.product_id,
                    "quantity": item_data.quantity,
                }
            )

        return await self.get_cart(user_id)

    async def remove_item(self, user_id: int, product_id: int) -> CartRead:
        cart = await self.cart_repo.find_one(user_id=user_id)
        if not cart:
            raise NotFoundException("Cart not found")

        item = await self.cart_item_repo.find_one(
            cart_id=cart.id, product_id=product_id
        )
        if not item:
            raise NotFoundException("Item not found in cart")

        await self.cart_item_repo.delete_one(item.id)
        return await self.get_cart(user_id)

    async def clear_cart(self, user_id: int) -> CartRead:
        cart = await self.cart_repo.find_one(user_id=user_id)
        if not cart:
            raise NotFoundException("Cart not found")

        await self.cart_item_repo.delete_all(cart_id=cart.id)
        return await self.get_cart(user_id)
