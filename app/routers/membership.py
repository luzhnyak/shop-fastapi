from fastapi import APIRouter, Depends, status
from app.services.membership import MembershipService
from app.schemas.membership import (
    MembershipResponse,
)
from app.utils.deps import get_current_user, get_membership_service
from app.schemas.user import UserResponse

router = APIRouter(prefix="/memberships", tags=["Company Memberships"])


@router.post(
    "/company/{company_id}/request",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
async def request_to_join(
    company_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.request_to_join(company_id, current_user.id)


@router.post(
    "/company/{company_id}/invite/{user_id}",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
async def invite_user(
    company_id: int,
    user_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.invite_user(company_id, user_id, current_user.id)


@router.patch(
    "/{membership_id}/accept-invite",
    response_model=MembershipResponse,
)
async def accept_invite(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.accept_invite(membership_id, current_user.id)


@router.delete("/{membership_id}/cancel-invite")
async def cancel_invite(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    await service.cancel_invite(membership_id, current_user.id)
    return {"detail": "Invitation declined"}


@router.patch(
    "/{membership_id}/accept-request",
    response_model=MembershipResponse,
)
async def accept_request(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.accept_request(membership_id, current_user.id)


@router.delete("/{membership_id}/cancel-request")
async def cancel_request(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    await service.cancel_request(membership_id, current_user.id)
    return {"detail": "Membership request declined"}


@router.delete("/{membership_id}/leave")
async def leave_company(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    await service.leave_company(membership_id, current_user.id)
    return {"detail": "Left company successfully"}


@router.delete("/{membership_id}/remove")
async def remove_member(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    await service.remove_member(membership_id, current_user.id)
    return {"detail": "User removed from company"}


@router.patch(
    "/{membership_id}/add-to-admin",
    response_model=MembershipResponse,
)
async def accept_request(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.add_to_admin(membership_id, current_user.id)


@router.patch(
    "/{membership_id}/remove-from-admin",
    response_model=MembershipResponse,
)
async def accept_request(
    membership_id: int,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.remove_from_admin(membership_id, current_user.id)


@router.get("/company/{company_id}/user/{user_id}", response_model=MembershipResponse)
async def get_membership(
    company_id: int,
    user_id: int,
    service: MembershipService = Depends(get_membership_service),
):
    return await service.get_membership(company_id, user_id)
