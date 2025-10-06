from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.review import ReviewRepository
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewRead,
    ReviewList,
)


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.review_repo = ReviewRepository(db)

    async def create_review(
        self, user_id: int, review_data: ReviewCreate
    ) -> ReviewRead:
        # Один користувач може залишити тільки один відгук на продукт
        existing = await self.review_repo.find_one(
            user_id=user_id, product_id=review_data.product_id
        )
        if existing:
            raise ConflictException("You have already left a review for this product")

        new_review = await self.review_repo.add_one(
            {
                "user_id": user_id,
                "product_id": review_data.product_id,
                "rating": review_data.rating,
                "comment": review_data.comment,
            }
        )
        return ReviewRead.model_validate(new_review)

    async def get_reviews(self, skip: int = 0, limit: int = 10) -> ReviewList:
        total = await self.review_repo.count_all()
        page = (skip // limit) + 1
        reviews = await self.review_repo.find_many(skip=skip, limit=limit)
        return ReviewList(
            items=[ReviewRead.model_validate(r) for r in reviews],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_review(self, review_id: int) -> ReviewRead:
        review = await self.review_repo.find_one(id=review_id)
        if not review:
            raise NotFoundException(f"Review with id {review_id} not found")
        return ReviewRead.model_validate(review)

    async def update_review(
        self, review_id: int, user_id: int, review_data: ReviewUpdate
    ) -> ReviewRead:
        review = await self.review_repo.find_one(id=review_id)
        if not review:
            raise NotFoundException(f"Review with id {review_id} not found")

        if review.user_id != user_id:
            raise BadRequestException("You can update only your own reviews")

        update_data = review_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_review = await self.review_repo.edit_one(review_id, update_data)
        return ReviewRead.model_validate(updated_review)

    async def delete_review(self, review_id: int, user_id: int) -> ReviewRead:
        review = await self.review_repo.find_one(id=review_id)
        if not review:
            raise NotFoundException(f"Review with id {review_id} not found")

        if review.user_id != user_id:
            raise BadRequestException("You can delete only your own reviews")

        deleted_review = await self.review_repo.delete_one(review_id)
        return ReviewRead.model_validate(deleted_review)
