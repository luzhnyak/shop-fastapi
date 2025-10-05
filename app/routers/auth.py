from fastapi import APIRouter, Depends, Request, Response
import logging

from app.schemas.user import SignInRequest, SignUpRequest, UserRead
from app.schemas.auth import Auth0Token, TokenResponse
from app.services.auth import AuthService
from app.utils.deps import get_auth_service, get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/register", response_model=TokenResponse)
async def register(
    data: SignUpRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.register(data)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * settings.app.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return result


@router.post("/login", response_model=TokenResponse)
async def login(
    data: SignInRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(data)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * settings.app.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return result


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    result = await service.refresh_token(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * settings.app.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return result


@router.post("/auth0-login", response_model=TokenResponse)
async def auth0_login(
    data: Auth0Token,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.auth0_login(data)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * settings.app.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return result


@router.post("/logout")
async def logout(response: Response):

    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        secure=True,
        samesite="Strict",
        expires=0,
    )

    return {"detail": "Logged out successfully"}
