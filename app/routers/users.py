from fastapi import APIRouter, Depends, status
import logging

from app.schemas.company import CompaniesListResponse, CompanyResponse
from app.schemas.membership import MembershipListResponse, MembershipStatus
from app.schemas.user import (
    SignUpRequest,
    UserResponse,
    UserUpdateRequest,
    UsersListResponse,
)

from app.services.membership import MembershipService
from app.services.user import UserService
from app.utils.deps import (
    get_company_service,
    get_current_user,
    get_membership_service,
    get_user_service,
)

router = APIRouter(prefix="/users", tags=["Users"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: SignUpRequest, service: UserService = Depends(get_user_service)
):
    db_user = await service.create_user(user)
    logger.info(f"User created: {db_user.first_name}")
    return db_user


@router.get("/", response_model=UsersListResponse)
async def get_users(
    skip: int = 0, limit: int = 10, service: UserService = Depends(get_user_service)
):
    return await service.get_users(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_user = await service.update_user(user_id, user_data, current_user.id)
    logger.info(f"User updated: {updated_user.first_name}")
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    deleted_user = await service.delete_user(user_id, current_user.id)
    logger.info(f"User deleted: {deleted_user.first_name}")
    return {
        "detail": f"User {deleted_user.first_name} {deleted_user.last_name} deleted"
    }


@router.get("/{user_id}/companies", response_model=MembershipListResponse)
async def get_user_companies(
    user_id: int,
    role: str = MembershipStatus.MEMBER,
    skip: int = 0,
    limit: int = 10,
    service: MembershipService = Depends(get_membership_service),
):
    return await service.get_user_companies(user_id, role, skip, limit)


@router.get("/{user_id}/available-companies", response_model=CompaniesListResponse)
async def get_available_companies(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    service: MembershipService = Depends(get_membership_service),
    current_user: CompanyResponse = Depends(get_current_user),
):
    return await service.get_available_companies(user_id, current_user.id, skip, limit)
