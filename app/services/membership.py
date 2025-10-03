from app.core.exceptions import (
    BadRequestException,
    DatabaseException,
    ForbiddenException,
    NotFoundException,
)
from app.repositories.company import CompanyRepository
from app.repositories.membership import MembershipRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.company import CompaniesListResponse, CompanyResponse
from app.schemas.membership import (
    MembershipListResponse,
    MembershipResponse,
    MembershipWithNameResponse,
    MembershipStatus,
)


class MembershipService:
    def __init__(self, db: AsyncSession):
        self.membership_repo = MembershipRepository(db)
        self.company_repo = CompanyRepository(db)
        self.db = db

    async def invite_user(
        self, company_id: int, user_id: int, owner_id: int
    ) -> MembershipResponse:
        company = await self.company_repo.find_one(id=company_id)
        if not company:
            raise NotFoundException("Company not found.")
        if company.owner_id != owner_id:
            raise ForbiddenException("You are not the owner of this company.")

        existing_membership = await self.membership_repo.find_one(
            company_id=company_id, user_id=user_id
        )
        if existing_membership:
            raise BadRequestException(
                "User is already a member or has a pending invitation/request."
            )

        new_invitation = await self.membership_repo.add_one(
            {
                "company_id": company_id,
                "user_id": user_id,
                "status": MembershipStatus.PENDING_INVITE,
            }
        )
        return MembershipResponse.model_validate(new_invitation)

    async def cancel_invitation(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        invitation = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.PENDING_INVITE,
        )
        if not invitation:
            raise NotFoundException("Invitation not found.")
        delete_membership = await self.membership_repo.delete_one(invitation.id)
        return MembershipResponse.model_validate(delete_membership)

    async def request_to_join(
        self, company_id: int, user_id: int
    ) -> MembershipResponse:
        company = await self.company_repo.find_one(id=company_id)
        if not company:
            raise NotFoundException("Company not found.")

        existing_membership = await self.membership_repo.find_one(
            company_id=company_id, user_id=user_id
        )
        if existing_membership:
            raise BadRequestException("You have already requested or are a member.")

        try:
            new_request = await self.membership_repo.add_one(
                {
                    "company_id": company_id,
                    "user_id": user_id,
                    "status": MembershipStatus.PENDING_REQUEST,
                }
            )
        except Exception as e:
            raise DatabaseException(str(e))
        return MembershipResponse.model_validate(new_request)

    async def cancel_request(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        request = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.PENDING_REQUEST,
        )
        if not request:
            raise NotFoundException("Request not found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=request.company_id
        )

        if not company and request.user_id != current_user_id:
            raise ForbiddenException(
                "You are not the owner of this company or the user."
            )

        delete_request = await self.membership_repo.delete_one(request.id)
        return MembershipResponse.model_validate(delete_request)

    async def accept_invite(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        invitation = await self.membership_repo.find_one(
            id=membership_id,
            user_id=current_user_id,
            status=MembershipStatus.PENDING_INVITE,
        )
        if not invitation:
            raise NotFoundException("No invitation found.")

        updated = await self.membership_repo.edit_one(
            invitation.id, {"status": MembershipStatus.MEMBER}
        )
        return MembershipResponse.model_validate(updated)

    async def cancel_invite(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:

        invitation = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.PENDING_INVITE,
        )
        if not invitation:
            raise NotFoundException("No invitation found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=invitation.company_id
        )

        if not company and invitation.user_id != current_user_id:
            raise ForbiddenException(
                "You are not the owner of this company or the user."
            )
        delete_invitation = await self.membership_repo.delete_one(invitation.id)
        return MembershipResponse.model_validate(delete_invitation)

    async def accept_request(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        request = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.PENDING_REQUEST,
        )
        if not request:
            raise NotFoundException("No request found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=request.company_id
        )

        if not company:
            raise ForbiddenException("You are not the owner of this company.")

        updated = await self.membership_repo.edit_one(
            request.id, {"status": MembershipStatus.MEMBER}
        )
        return MembershipResponse.model_validate(updated)

    async def cancel_request(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:

        request = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.PENDING_REQUEST,
        )
        if not request:
            raise NotFoundException("No request found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=request.company_id
        )

        if not company and request.user_id != current_user_id:
            raise ForbiddenException(
                "You are not the owner of this company or the user."
            )

        delete_request = await self.membership_repo.delete_one(request.id)
        return MembershipResponse.model_validate(delete_request)

    async def remove_member(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:

        member = await self.membership_repo.find_one(
            id=membership_id, status=MembershipStatus.MEMBER
        )
        if not member:
            raise NotFoundException("User is not a member.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=member.company_id
        )

        if not company:
            raise ForbiddenException("You are not the owner of this company.")

        delete_member = await self.membership_repo.delete_one(member.id)
        return MembershipResponse.model_validate(delete_member)

    async def leave_company(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        member = await self.membership_repo.find_one(
            id=membership_id, user_id=current_user_id, status=MembershipStatus.MEMBER
        )
        if not member:
            raise NotFoundException("You are not a member.")

        delete_member = await self.membership_repo.delete_one(member.id)
        return MembershipResponse.model_validate(delete_member)

    async def add_to_admin(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        member = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.MEMBER,
        )
        if not member:
            raise NotFoundException("No member found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=member.company_id
        )

        if not company:
            raise ForbiddenException("You are not the owner of this company.")

        updated = await self.membership_repo.edit_one(
            member.id, {"status": MembershipStatus.ADMIN}
        )
        return MembershipResponse.model_validate(updated)

    async def remove_from_admin(
        self, membership_id: int, current_user_id: int
    ) -> MembershipResponse:
        member = await self.membership_repo.find_one(
            id=membership_id,
            status=MembershipStatus.ADMIN,
        )
        if not member:
            raise NotFoundException("No member found.")

        company = await self.company_repo.find_one(
            owner_id=current_user_id, id=member.company_id
        )

        if not company:
            raise ForbiddenException("You are not the owner of this company.")

        updated = await self.membership_repo.edit_one(
            member.id, {"status": MembershipStatus.MEMBER}
        )
        return MembershipResponse.model_validate(updated)

    async def get_membership(
        self,
        company_id: int,
        user_id: int,
    ) -> MembershipResponse:

        membership = await self.membership_repo.find_one(
            company_id=company_id,
            user_id=user_id,
        )
        if not membership:
            return MembershipWithNameResponse(
                id=0,
                company_id=company_id,
                user_id=user_id,
                name="",
                status=MembershipStatus.NONE,
            )

        return MembershipResponse.model_validate(membership)

    async def get_members(
        self,
        company_id: int,
        current_user_id: int,
        role: str = MembershipStatus.MEMBER,
        skip: int = 0,
        limit: int = 10,
    ) -> MembershipListResponse:
        total = await self.membership_repo.count_all(company_id=company_id, status=role)
        members = await self.membership_repo.find_members(company_id, role, skip, limit)

        if (
            role == MembershipStatus.PENDING_INVITE
            or role == MembershipStatus.PENDING_REQUEST
        ):
            await self._check_company_permission(company_id, current_user_id)

        return MembershipListResponse(
            items=[
                MembershipWithNameResponse(
                    id=member[0].id,
                    company_id=member[0].company_id,
                    user_id=member[0].user_id,
                    name=f"{member[1]} {member[2]}",
                    status=member[0].status,
                )
                for member in members
            ],
            total=total,
            page=(skip // limit) + 1,
            per_page=limit,
        )

    async def get_user_companies(
        self,
        user_id: int,
        role: str = MembershipStatus.MEMBER,
        skip: int = 0,
        limit: int = 10,
    ) -> MembershipListResponse:
        total = await self.membership_repo.count_all(user_id=user_id, status=role)
        companies = await self.membership_repo.find_company(
            user_id,
            role,
            skip,
            limit,
        )
        return MembershipListResponse(
            items=[
                MembershipWithNameResponse(
                    id=company[0].id,
                    company_id=company[0].company_id,
                    user_id=company[0].user_id,
                    name=company[1],
                    status=company[0].status,
                )
                for company in companies
            ],
            total=total,
            page=(skip // limit) + 1,
            per_page=limit,
        )

    async def get_available_companies(
        self, user_id: int, owner_id: int, skip: int = 0, limit: int = 10
    ):
        total = await self.membership_repo.count_companies_without_user(
            user_id, owner_id
        )
        page = (skip // limit) + 1
        companies = await self.membership_repo.find_companies_without_user(
            user_id, owner_id, skip, limit
        )
        return CompaniesListResponse(
            items=[CompanyResponse.model_validate(company) for company in companies],
            total=total,
            page=page,
            per_page=limit,
        )

    async def _check_company_permission(self, company_id: int, user_id: int) -> None:
        membership = await MembershipRepository(self.db).find_one(
            company_id=company_id, user_id=user_id
        )
        company = await CompanyRepository(self.db).find_one(id=company_id)

        if (
            not membership or membership.status != MembershipStatus.ADMIN
        ) and company.owner_id != user_id:
            raise ForbiddenException("You do not have permission.")
