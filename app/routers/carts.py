from fastapi import APIRouter, Depends, status
import logging


from app.schemas.cart import CartCreate, CartUpdate, CartRead, CartList

from app.services.cart import CartService
from app.utils.deps import get_cart_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
async def create_cart(
    cart: CartCreate, service: CartService = Depends(get_cart_service)
):
    db_cart = await service.create_cart(cart)
    logger.info(f"Cart created: {db_cart.id}")
    return db_cart


@router.get("/", response_model=CartList)
async def get_carts(
    skip: int = 0, limit: int = 10, service: CartService = Depends(get_cart_service)
):
    return await service.get_carts(skip, limit)


@router.get("/{cart_id}", response_model=CartRead)
async def get_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    cart = await service.get_cart(cart_id)
    return cart


@router.put("/{cart_id}", response_model=CartRead)
async def update_cart(
    cart_id: int,
    cart_data: CartUpdate,
    service: CartService = Depends(get_cart_service),
):
    updated_cart = await service.update_cart(cart_id, cart_data)
    logger.info(f"Cart updated: {updated_cart.id}")
    return updated_cart


@router.delete("/{cart_id}")
async def delete_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    deleted_cart = await service.delete_cart(cart_id)
    logger.info(f"Cart deleted: {deleted_cart.id}")
    return {"detail": f"Cart {deleted_cart.id} deleted"}
