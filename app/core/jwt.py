from datetime import datetime, timedelta, UTC

from fastapi import HTTPException
import requests
from app.core.config import settings
from jose import JWTError, jwt


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.app.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.app.SECRET_KEY, algorithm=settings.app.ALGORITHM
    )


def create_refresh_token(data: dict):
    expire = datetime.now(UTC) + timedelta(days=settings.app.REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, settings.app.SECRET_KEY, algorithm=settings.app.ALGORITHM)


def verify_access_token(token: str) -> dict | None:

    payload = jwt.decode(
        token, settings.app.SECRET_KEY, algorithms=[settings.app.ALGORITHM]
    )
    return payload


def get_auth0_public_key():
    jwks_url = f"https://{settings.app.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get JWKS")
    return response.json()


def verify_auth0_token(token: str):
    try:
        jwks = get_auth0_public_key()
        header = jwt.get_unverified_header(token)

        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if not rsa_key:
            raise HTTPException(
                status_code=401, detail="Invalid Auth0 token (no valid key)"
            )

        payload = jwt.decode(
            token, rsa_key, algorithms=["RS256"], audience=settings.app.AUTH0_AUDIENCE
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid Auth0 token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Auth0 token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid audience in Auth0 token")
