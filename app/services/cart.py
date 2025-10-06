from app.core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cart import CartRepository, CartItemRepository

from app.schemas.cart import (
    CartList,
    CartRead,
    CartItemCreate,
    CartItemRead,
    CartReadMin,
)


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemRepository(db)

    async def get_cart(self, user_id: int) -> CartRead:
        cart = await self.cart_repo.find_one_cart(user_id=user_id)
        if not cart:
            # якщо кошика ще нема — створюємо
            cart = await self.cart_repo.add_one({"user_id": user_id})

        items = await self.cart_item_repo.find_all(cart_id=cart.id)
        cart_dict = CartRead.model_validate(cart).model_dump()
        cart_dict["items"] = [CartItemRead.model_validate(i) for i in items]

        return CartRead(**cart_dict)

    async def get_carts(self, skip: int = 0, limit: int = 10) -> CartList:
        total = await self.cart_repo.count_all()
        page = (skip // limit) + 1
        orders = await self.cart_repo.find_many(skip=skip, limit=limit)
        return CartList(
            items=[CartReadMin.model_validate(o) for o in orders],
            total=total,
            page=page,
            per_page=limit,
        )

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
