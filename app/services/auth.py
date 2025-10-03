from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from jose import ExpiredSignatureError, JWTError, jwt
from http import HTTPStatus

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    UnauthorizedException,
)
from app.schemas.auth import Auth0Token, Token
from app.schemas.user import SignInRequest, SignUpRequest
from app.core.jwt import create_access_token, create_refresh_token
from app.core.config import settings
from app.services.user import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_service = UserService(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def register(self, user_data: SignUpRequest) -> Token:
        user = await self.user_service.get_user_by_email(user_data.email)
        if user:
            raise ConflictException("User with this email already exists")

        new_user = await self.user_service.create_user(user_data)

        access_token = create_access_token({"sub": new_user.email})
        refresh_token = create_refresh_token({"sub": new_user.email})

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def login(self, user_data: SignInRequest) -> Token:
        user = await self.user_service.get_user_by_email(user_data.email)

        if not user or not self.verify_password(
            user_data.password, user.hashed_password
        ):
            raise UnauthorizedException(detail="Invalid credentials")

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def auth0_login(self, data: Auth0Token) -> Token:
        response_AUTH0 = requests.get(
            f"https://{settings.app.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {data.token}"},
        )

        if response_AUTH0.status_code != HTTPStatus.OK:
            raise BadRequestException(detail="Invalid Auth0 token")

        user_data = response_AUTH0.json()
        user = await self.user_service.get_user_by_email(user_data["email"])

        if not user:
            user = await self.user_service.create_user(
                SignUpRequest(
                    first_name=user_data["given_name"],
                    last_name=user_data["family_name"],
                    email=user_data["email"],
                    password="password",
                )
            )

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token: str) -> Token:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.app.SECRET_KEY,
                algorithms=[settings.app.ALGORITHM],
            )
            email = payload.get("sub")
            if email is None:
                raise UnauthorizedException(detail="Invalid refresh token")

            access_token = create_access_token({"sub": email})
            new_refresh_token = create_refresh_token({"sub": email})

            return Token(access_token=access_token, refresh_token=new_refresh_token)
        except ExpiredSignatureError:
            raise UnauthorizedException(detail="Refresh token expired")
        except JWTError:
            raise UnauthorizedException(detail="Invalid refresh token")
