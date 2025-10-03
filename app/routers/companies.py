from fastapi import APIRouter, Depends, status
import logging

from app.schemas.company import (
    CompanyCreateRequest,
    CompanyResponse,
    CompanyUpdateRequest,
    CompaniesListResponse,
    CompanyVisibilityUpdateRequest,
)
from app.schemas.membership import MembershipListResponse, MembershipStatus
from app.schemas.user import UserResponse
from app.services.company import CompanyService
from app.services.membership import MembershipService
from app.utils.deps import get_company_service, get_current_user, get_membership_service

router = APIRouter(prefix="/companies", tags=["Companies"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreateRequest,
    service: CompanyService = Depends(get_company_service),
    current_user: CompanyResponse = Depends(get_current_user),
):
    db_company = await service.create_company(company, current_user.id)
    logger.info(f"Company created: {db_company.name}")
    return db_company


@router.get("/", response_model=CompaniesListResponse)
async def get_companies(
    skip: int = 0,
    limit: int = 10,
    service: CompanyService = Depends(get_company_service),
):
    return await service.get_companies(skip, limit)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int, service: CompanyService = Depends(get_company_service)
):
    company = await service.get_company(company_id)
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyUpdateRequest,
    service: CompanyService = Depends(get_company_service),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_company = await service.update_company(
        company_id, company_data, current_user.id
    )
    logger.info(f"Company updated: {updated_company.name}")
    return updated_company


@router.patch("/{company_id}/visibility", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyVisibilityUpdateRequest,
    service: CompanyService = Depends(get_company_service),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_company = await service.update_company_visibility(
        company_id, company_data.visibility, current_user.id
    )
    logger.info(f"Company visibility updated: {updated_company.name}")
    return updated_company


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service),
    current_user: UserResponse = Depends(get_current_user),
):
    deleted_company = await service.delete_company(company_id, current_user.id)
    logger.info(f"Company deleted: {deleted_company.name}")
    return {"detail": f"Company {deleted_company.name} deleted"}


@router.get("/{company_id}/members", response_model=MembershipListResponse)
async def get_members(
    company_id: int,
    role: str = MembershipStatus.MEMBER,
    skip: int = 0,
    limit: int = 10,
    service: MembershipService = Depends(get_membership_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.get_members(company_id, current_user.id, role, skip, limit)
