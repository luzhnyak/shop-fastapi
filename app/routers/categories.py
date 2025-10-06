from typing import List
from fastapi import APIRouter, Depends, status
import logging

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
)

from app.services.category import CategoryService

from app.utils.deps import get_category_service

router = APIRouter(tags=["Categories", "Products"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, service: CategoryService = Depends(get_category_service)
):
    db_category = await service.create_category(category)
    logger.info(f"Category created: {db_category.name}")
    return db_category


@router.get("/", response_model=List[CategoryRead])
async def get_categories(
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_categories()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int, service: CategoryService = Depends(get_category_service)
):
    category = await service.get_category(category_id)
    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    updated_category = await service.update_category(category_id, category_data)
    logger.info(f"Category updated: {updated_category.name}")
    return updated_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int, service: CategoryService = Depends(get_category_service)
):
    deleted_category = await service.delete_category(category_id)
    logger.info(f"Category deleted: {deleted_category.name}")
    return {"detail": f"Category {deleted_category.name} deleted"}
