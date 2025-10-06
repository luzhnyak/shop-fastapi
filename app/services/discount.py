from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.repositories.discount import DiscountRepository
from app.schemas.discount import (
    DiscountCreate,
    DiscountUpdate,
    DiscountRead,
    DiscountList,
)


class DiscountService:
    def __init__(self, db: AsyncSession):
        self.discount_repo = DiscountRepository(db)

    async def create_discount(self, discount_data: DiscountCreate) -> DiscountRead:
        existing = await self.discount_repo.find_one(code=discount_data.code)
        if existing:
            raise ConflictException("Discount with this code already exists")

        new_discount = await self.discount_repo.add_one(discount_data.model_dump())
        return DiscountRead.model_validate(new_discount)

    async def get_discounts(self, skip: int = 0, limit: int = 10) -> DiscountList:
        total = await self.discount_repo.count_all()
        page = (skip // limit) + 1
        discounts = await self.discount_repo.find_many(skip=skip, limit=limit)
        return DiscountList(
            items=[DiscountRead.model_validate(d) for d in discounts],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_discount(self, discount_id: int) -> DiscountRead:
        discount = await self.discount_repo.find_one(id=discount_id)
        if not discount:
            raise NotFoundException(f"Discount with id {discount_id} not found")
        return DiscountRead.model_validate(discount)

    async def get_discount_by_code(self, code: str) -> DiscountRead:
        discount = await self.discount_repo.find_one(code=code)
        if not discount:
            raise NotFoundException(f"Discount with code {code} not found")

        # Перевіряємо чи активна і чи входить в діапазон дат
        now = datetime.utcnow()
        if not discount.active or not (
            (not discount.valid_from or discount.valid_from <= now)
            and (not discount.valid_to or discount.valid_to >= now)
        ):
            raise BadRequestException("Discount is not active")

        return DiscountRead.model_validate(discount)

    async def update_discount(
        self, discount_id: int, discount_data: DiscountUpdate
    ) -> DiscountRead:
        discount = await self.get_discount(discount_id)

        update_data = discount_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_discount = await self.discount_repo.edit_one(discount_id, update_data)
        return DiscountRead.model_validate(updated_discount)

    async def delete_discount(self, discount_id: int) -> DiscountRead:
        discount = await self.get_discount(discount_id)
        deleted_discount = await self.discount_repo.delete_one(discount_id)
        return DiscountRead.model_validate(deleted_discount)
