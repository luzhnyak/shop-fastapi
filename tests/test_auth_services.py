import pytest
from app.services.auth import AuthService
from app.schemas.user import SignUpRequest, SignInRequest


@pytest.mark.asyncio
async def test_service_register(db_session):
    service = AuthService(db_session)
    user_data = SignUpRequest(first_name="Test", last_name="User4",
                              email="testuser4@example.com", password="password4")

    result = await service.register(user_data)
    assert isinstance(result.access_token, str)
    assert isinstance(result.refresh_token, str)


@pytest.mark.asyncio
async def test_service_login(db_session):
    service = AuthService(db_session)

    user_data = SignInRequest(
        email="testuser4@example.com", password="password4")

    result = await service.login(user_data)
    assert isinstance(result.access_token, str)
    assert isinstance(result.refresh_token, str)
