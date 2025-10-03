from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    email: str


class Auth0Token(BaseModel):
    token: str
