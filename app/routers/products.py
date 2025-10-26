from fastapi import APIRouter, Depends, status
from logger import logger

from app.schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductList
from app.services.product import ProductService
from app.utils.deps import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    db_product = await service.create_product(product)
    logger.info(f"Product created: {db_product.name}")
    return db_product


@router.get("/", response_model=ProductList)
async def get_products(
    skip: int = 0,
    limit: int = 10,
    category_id: int = None,
    category: str = None,
    service: ProductService = Depends(get_product_service),
):

    filters = {
        k: v
        for k, v in {
            "category_id": category_id,
            "category": category,
        }.items()
        if v is not None
    }

    return await service.get_products(skip, limit, **filters)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    product = await service.get_product(product_id)
    return product


@router.get("/slug/{slug}", response_model=ProductRead)
async def get_product_by_slug(
    slug: str, service: ProductService = Depends(get_product_service)
):
    product = await service.get_product_by_slug(slug)
    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    updated_product = await service.update_product(product_id, product_data)
    logger.info(f"Product updated: {updated_product.name}")
    return updated_product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    deleted_product = await service.delete_product(product_id)
    logger.info(f"Product deleted: {deleted_product.name}")
    return {"detail": f"Product {deleted_product.name} deleted"}
