from typing import List
import uuid

from slugify import slugify
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.category import CategoryRepository

from app.schemas.category import (
    CategoryCreate,
    CategoryList,
    CategoryUpdate,
    CategoryRead,
)
from app.services.base import BaseService


class CategoryService(BaseService):
    def __init__(self, db: AsyncSession):
        self.category_repo = CategoryRepository(db)

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        existing_category = await self.category_repo.find_one(name=category_data.name)
        if existing_category:
            raise ConflictException("Category with this name already exists")

        category_data.slug = await self._generate_unique_slug(
            name=category_data.name, repo=self.category_repo, slug_field="slug"
        )

        new_category = await self.category_repo.add_one(category_data.model_dump())
        return CategoryRead.model_validate(new_category)

    async def get_all_categories(self) -> CategoryList:
        total = await self.category_repo.count_all()
        categories = await self.category_repo.find_all()
        return CategoryList(
            items=[CategoryRead.model_validate(r) for r in categories],
            total=total,
            page=1,
            per_page=total,
        )

    async def get_categories(self, skip: int = 0, limit: int = 10) -> CategoryList:
        total = await self.category_repo.count_all()
        page = (skip // limit) + 1
        categories = await self.category_repo.find_many(skip=skip, limit=limit)
        return CategoryList(
            items=[CategoryRead.model_validate(r) for r in categories],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_category(self, category_id: int) -> CategoryRead:
        category = await self.category_repo.find_one(id=category_id)
        if not category:
            raise NotFoundException(f"Category with id {category_id} not found")
        return CategoryRead.model_validate(category)

    async def get_category_by_slug(self, slug: str) -> CategoryRead:
        category = await self.category_repo.find_one(slug=slug)
        if not category:
            raise NotFoundException(f"Category with slug {slug} not found")
        return CategoryRead.model_validate(category)

    async def update_category(
        self, category_id: int, category_data: CategoryUpdate
    ) -> CategoryRead:
        category = await self.get_category(category_id)

        update_data = category_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_category = await self.category_repo.edit_one(category_id, update_data)
        return CategoryRead.model_validate(updated_category)

    async def delete_category(self, category_id: int) -> CategoryRead:
        category = await self.get_category(category_id)
        deleted_category = await self.category_repo.delete_one(category_id)
        return CategoryRead.model_validate(deleted_category)
