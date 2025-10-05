from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.wishlist import WishlistRepository
from app.schemas.wishlist import (
    WishlistCreate,
    WishlistRead,
    WishlistList,
)


class WishlistService:
    def __init__(self, db: AsyncSession):
        self.wishlist_repo = WishlistRepository(db)

    async def add_to_wishlist(self, wishlist_data: WishlistCreate) -> WishlistRead:
        existing = await self.wishlist_repo.find_one(
            user_id=wishlist_data.user_id, product_id=wishlist_data.product_id
        )
        if existing:
            raise ConflictException("Product already exists in wishlist")

        new_item = await self.wishlist_repo.add_one(wishlist_data.model_dump())
        return WishlistRead.model_validate(new_item)

    async def get_wishlist(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> WishlistList:
        total = await self.wishlist_repo.count_all(user_id=user_id)
        page = (skip // limit) + 1
        items = await self.wishlist_repo.find_all(
            user_id=user_id, skip=skip, limit=limit
        )
        return WishlistList(
            items=[WishlistRead.model_validate(i) for i in items],
            total=total,
            page=page,
            per_page=limit,
        )

    async def remove_from_wishlist(self, user_id: int, product_id: int) -> WishlistRead:
        item = await self.wishlist_repo.find_one(user_id=user_id, product_id=product_id)
        if not item:
            raise NotFoundException("Product not found in wishlist")

        deleted_item = await self.wishlist_repo.delete_one(item.id)
        return WishlistRead.model_validate(deleted_item)

    async def clear_wishlist(self, user_id: int) -> None:
        items = await self.wishlist_repo.find_all(user_id=user_id)
        if not items:
            raise BadRequestException("Wishlist is already empty")

        for i in items:
            await self.wishlist_repo.delete_one(i.id)
