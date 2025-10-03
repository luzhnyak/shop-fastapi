from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import verify_access_token
from app.db.db import get_db
from app.core.exceptions import ServerException, UnauthorizedException
from app.db.redis import RedisService
from app.schemas.user import UserResponse
from app.services.auth import AuthService
from app.services.company import CompanyService
from app.services.membership import MembershipService
from app.services.quiz import QuizService
from app.services.quiz_export_service import QuizExportService
from app.services.quiz_result import QuizResultService
from app.services.quiz_result_redis import QuizResultRedisService
from app.services.user import UserService


auth_token_schemas = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_company_service(db: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(db)


def get_membership_service(db: AsyncSession = Depends(get_db)) -> MembershipService:
    return MembershipService(db)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_token_schemas),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        payload = verify_access_token(token.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException(detail="Invalid token")

        user = await service.get_user_by_email(email)
        return UserResponse.model_validate(user)

    except JWTError:
        raise UnauthorizedException(detail="Invalid token")
    except Exception as e:
        raise ServerException(detail=str(e))


async def get_quiz_service(db: AsyncSession = Depends(get_db)) -> QuizService:
    return QuizService(db)


async def get_quiz_result_service(
    db: AsyncSession = Depends(get_db),
    redis: RedisService = Depends(),
) -> QuizResultService:
    return QuizResultService(db, redis)


async def get_quiz_result_redis_service(
    db: AsyncSession = Depends(get_db),
    redis: RedisService = Depends(),
) -> QuizResultRedisService:
    return QuizResultRedisService(db, redis)


async def get_quiz_export_service(
    db: AsyncSession = Depends(get_db),
    redis: RedisService = Depends(),
) -> QuizExportService:
    return QuizExportService(db, redis)
