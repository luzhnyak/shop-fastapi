from typing import List
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.category import CategoryRepository

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repo = CategoryRepository(db)

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        category = await self.category_repo.find_one(name=category_data.name)
        if category:
            raise ConflictException("Category with this name already exists")

        new_category = await self.category_repo.add_one(category_data.model_dump())
        return CategoryRead.model_validate(new_category)

    async def get_categories(self) -> List[CategoryRead]:
        categories = await self.category_repo.find_all()
        return [CategoryRead.model_validate(c) for c in categories]

    async def get_category(self, category_id: int) -> CategoryRead:
        category = await self.category_repo.find_one(id=category_id)
        if not category:
            raise NotFoundException(f"Category with id {category_id} not found")
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
