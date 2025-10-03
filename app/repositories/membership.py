from sqlalchemy import func, select
from app.models.company import Company
from app.models.membership import Membership, MembershipStatus
from app.models.user import User
from app.utils.repository import SQLAlchemyRepository


class MembershipRepository(SQLAlchemyRepository):
    model = Membership

    async def find_members(
        self, company_id: int, status: MembershipStatus, skip: int, limit: int
    ):
        stmt = (
            select(self.model, User.first_name, User.last_name)
            .join(User, User.id == self.model.user_id)
            .filter(
                self.model.company_id == company_id,
                self.model.status == status,
            )
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return res.all()

    async def find_company(
        self, user_id: int, status: MembershipStatus, skip: int, limit: int
    ):
        stmt = (
            select(self.model, Company.name)
            .join(Company, Company.id == self.model.company_id)
            .filter(
                self.model.user_id == user_id,
                self.model.status == status,
            )
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return res.all()

    async def find_companies_without_user(
        self, user_id: int, owner_id: int, skip: int, limit: int
    ):
        subquery = (
            select(self.model.company_id)
            .filter(self.model.user_id == user_id)
            .scalar_subquery()
        )

        stmt = (
            select(Company)
            .where(
                ~Company.id.in_(subquery),
                Company.owner_id == owner_id,
            )
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def count_companies_without_user(self, user_id: int, owner_id: int):
        subquery = (
            select(self.model.company_id)
            .filter(self.model.user_id == user_id)
            .scalar_subquery()
        )

        stmt = (
            select(func.count())
            .select_from(Company)
            .where(
                ~Company.id.in_(subquery),
                Company.owner_id == owner_id,
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar()
