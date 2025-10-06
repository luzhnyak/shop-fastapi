from app.core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order import OrderRepository, OrderItemRepository

from app.schemas.order import (
    OrderCreate,
    OrderReadMin,
    OrderUpdate,
    OrderRead,
    OrderList,
    OrderItemCreate,
    OrderItemRead,
)


class OrderService:
    def __init__(self, db: AsyncSession):
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)

    async def create_order(self, order_data: OrderCreate) -> OrderRead:
        new_order = await self.order_repo.add_one(
            {
                "user_id": order_data.user_id,
                "address_id": order_data.address_id,
                "status": "pending",
            }
        )

        items = []
        for item in order_data.items:
            order_item = await self.order_item_repo.add_one(
                {
                    "order_id": new_order.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                }
            )
            items.append(OrderItemRead.model_validate(order_item))

        order_dict = OrderRead.model_validate(new_order).model_dump()
        order_dict["items"] = items
        return OrderRead(**order_dict)

    async def get_orders(self, skip: int = 0, limit: int = 10) -> OrderList:
        total = await self.order_repo.count_all()
        page = (skip // limit) + 1
        orders = await self.order_repo.find_many(skip=skip, limit=limit)
        return OrderList(
            items=[OrderReadMin.model_validate(o) for o in orders],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_order(self, order_id: int) -> OrderRead:
        order = await self.order_repo.find_one_order(id=order_id)
        if not order:
            raise NotFoundException(f"Order with id {order_id} not found")

        # items = await self.order_item_repo.find_all(order_id=order_id)
        # order_dict = OrderRead.model_validate(order).model_dump()
        # order_dict["items"] = [OrderItemRead.model_validate(i) for i in items]

        return OrderRead.model_validate(order)

    async def update_order(self, order_id: int, order_data: OrderUpdate) -> OrderRead:
        order = await self.get_order(order_id)

        update_data = order_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_order = await self.order_repo.edit_one(order_id, update_data)
        return OrderRead.model_validate(updated_order)

    async def delete_order(self, order_id: int) -> OrderRead:
        order = await self.get_order(order_id)
        deleted_order = await self.order_repo.delete_one(order_id)
        return OrderRead.model_validate(deleted_order)
