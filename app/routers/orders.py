from fastapi import APIRouter, Depends, status
import logging

from app.schemas.order import OrderCreate, OrderUpdate, OrderRead, OrderList

from app.services.order import OrderService

from app.utils.deps import get_order_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate, service: OrderService = Depends(get_order_service)
):
    db_order = await service.create_order(order)
    logger.info(f"Order created: {db_order.id}")
    return db_order


@router.get("/", response_model=OrderList)
async def get_orders(
    skip: int = 0, limit: int = 10, service: OrderService = Depends(get_order_service)
):
    return await service.get_orders(skip, limit)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    order = await service.get_order(order_id)
    return order


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    service: OrderService = Depends(get_order_service),
):
    updated_order = await service.update_order(order_id, order_data)
    logger.info(f"Order updated: {updated_order.id}")
    return updated_order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    deleted_order = await service.delete_order(order_id)
    logger.info(f"Order deleted: {deleted_order.id}")
    return {"detail": f"Order {deleted_order.id} deleted"}
