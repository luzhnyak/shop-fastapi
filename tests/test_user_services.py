import pytest
from unittest.mock import AsyncMock
from app.services.user import UserService
from app.schemas.user import SignUpRequest, UserResponse, UserUpdateRequest
from app.core.exceptions import ForbiddenException


@pytest.mark.asyncio
async def test_service_create_user(db_session):
    service = UserService(db_session)
    user_data = SignUpRequest(first_name="Test", last_name="User2",
                              email="testuser2@example.com", password="hashedpassword")

    user = await service.create_user(user_data)
    assert user.first_name == "Test"
    assert user.last_name == "User2"
    assert user.email == "testuser2@example.com"


@pytest.mark.asyncio
async def test_service_get_users(db_session):
    service = UserService(db_session)
    retrieved_users = await service.get_users()
    assert isinstance(retrieved_users.items, list)
    assert isinstance(retrieved_users.total, int)
    assert isinstance(retrieved_users.page, int)


@pytest.mark.asyncio
async def test_service_get_user(db_session):
    service = UserService(db_session)
    user_id = 2
    user = await service.get_user(user_id)
    assert user.id == user_id
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.email == "jane.smith@example.com"


@pytest.mark.asyncio
async def test_service_update_user(db_session):
    service = UserService(db_session)
    user_id = 2
    current_user_id = 2
    user_data = UserUpdateRequest(first_name="Updated", last_name="User",
                                  email="jane.smith@example.com", password="hashedpassword")

    user = await service.update_user(user_id, user_data, current_user_id)
    assert user.id == user_id
    assert user.first_name == "Updated"
    assert user.last_name == "User"
    assert user.email == "jane.smith@example.com"


@pytest.mark.asyncio
async def test_service_update_user_forbidden(db_session):
    service = UserService(db_session)
    user_id = 2
    current_user_id = 3

    user_data = UserUpdateRequest(
        first_name="Updated",
        last_name="User",
        password="newpassword"
    )

    with pytest.raises(ForbiddenException, match="You can only update your own profile"):
        await service.update_user(user_id, user_data, current_user_id)


@pytest.mark.asyncio
async def test_service_delete_user(db_session):
    service = UserService(db_session)
    user_id = 2
    current_user_id = 2
    user = await service.delete_user(user_id, current_user_id)
    assert user.id == user_id


@pytest.mark.asyncio
async def test_service_delete_user_forbidden(db_session):
    service = UserService(db_session)
    user_id = 2
    current_user_id = 3

    with pytest.raises(ForbiddenException, match="You can only delete your own account"):
        await service.delete_user(user_id, current_user_id)
