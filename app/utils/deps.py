from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import verify_access_token
from app.db.db import get_db
from app.core.exceptions import ServerException, UnauthorizedException
from app.db.redis import RedisService
from app.schemas.user import UserRead
from app.services.auth import AuthService
from app.services.cart import CartService
from app.services.order import OrderService
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.user import UserService


auth_token_schemas = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


def get_order_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(db)


def get_cart_service(db: AsyncSession = Depends(get_db)) -> CartService:
    return CartService(db)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_token_schemas),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    try:
        payload = verify_access_token(token.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException(detail="Invalid token")

        user = await service.get_user_by_email(email)
        return UserRead.model_validate(user)

    except JWTError:
        raise UnauthorizedException(detail="Invalid token")
    except Exception as e:
        raise ServerException(detail=str(e))
