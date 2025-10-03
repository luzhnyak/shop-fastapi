from fastapi.testclient import TestClient
from fastapi import status
import pytest


async def test_create_user(client: TestClient):
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "hashedpassword",
    }
    response = await client.post("/users/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert response.json()["email"] == "testuser@example.com"


@pytest.mark.asyncio
async def test_get_users(client: TestClient):
    response = await client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)
    assert isinstance(response.json()["total"], int)
    assert isinstance(response.json()["page"], int)


@pytest.mark.asyncio
async def test_get_user(client: TestClient):
    response = await client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "john.doe@example.com"


async def test_update_user(client: TestClient):
    user_id = 1
    update_data = {
        "first_name": "Updated",
        "last_name": "User",
        "email": "updateduser@example.com",
        "password": "hashedpassword",
    }
    response = await client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_delete_user(client: TestClient):
    user_id = 1
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
