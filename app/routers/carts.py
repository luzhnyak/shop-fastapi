from fastapi import APIRouter, Depends, status
from logger import logger

from app.schemas.cart import CartCreate, CartItemCreate, CartUpdate, CartRead, CartList

from app.services.cart import CartService
from app.utils.deps import get_cart_service

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/{user_id}", response_model=CartRead, status_code=status.HTTP_201_CREATED)
async def add_item(
    user_id: int,
    item_data: CartItemCreate,
    service: CartService = Depends(get_cart_service),
):
    cart = await service.add_item(user_id, item_data)
    logger.info(f"Item added to cart: {cart.id}")
    return cart


@router.get("/", response_model=CartList)
async def get_carts(
    skip: int = 0, limit: int = 10, service: CartService = Depends(get_cart_service)
):
    return await service.get_carts(skip, limit)


@router.get("/{user_id}", response_model=CartRead)
async def get_cart(user_id: int, service: CartService = Depends(get_cart_service)):
    cart = await service.get_cart(user_id)
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
