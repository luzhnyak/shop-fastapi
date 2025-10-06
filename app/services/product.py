from typing import List
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import (
    ProductImageRepository,
    ProductOptionRepository,
    ProductRepository,
)
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductList


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repo = ProductRepository(db)
        self.option_repo = ProductOptionRepository(db)
        self.image_repo = ProductImageRepository(db)

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        # можна перевірити унікальність імені товару
        product = await self.product_repo.find_one(name=product_data.name)
        if product:
            raise ConflictException("Product with this name already exists")

        new_product = await self.product_repo.add_one(
            product_data.model_dump(exclude={"options", "images"})
        )

        # додаємо options
        for option in product_data.options:
            await self.option_repo.add_one(
                {**option.model_dump(), "product_id": new_product.id}
            )

        # додаємо images
        for image in product_data.images:
            await self.image_repo.add_one(
                {**image.model_dump(), "product_id": new_product.id}
            )
        return ProductRead.model_validate(new_product)

    async def get_products(self, skip: int = 0, limit: int = 10) -> ProductList:
        total = await self.product_repo.count_all()
        page = (skip // limit) + 1
        products = await self.product_repo.find_many_products(skip=skip, limit=limit)
        return ProductList(
            items=[ProductRead.model_validate(p) for p in products],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_product(self, product_id: int) -> ProductRead:
        product = await self.product_repo.find_one_product(id=product_id)
        if not product:
            raise NotFoundException(f"Product with id {product_id} not found")
        return ProductRead.model_validate(product)

    async def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> ProductRead:
        product = await self.get_product(product_id)

        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_product = await self.product_repo.edit_one(product_id, update_data)

        return ProductRead.model_validate(updated_product)

    async def delete_product(self, product_id: int) -> ProductRead:
        product = await self.get_product(product_id)
        deleted_product = await self.product_repo.delete_one(product_id)
        return ProductRead.model_validate(deleted_product)
