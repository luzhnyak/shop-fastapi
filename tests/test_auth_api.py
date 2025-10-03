from fastapi.testclient import TestClient
from fastapi import status
import pytest


async def test_register(client: TestClient):
    data = {
        "first_name": "Test",
        "last_name": "User3",
        "email": "testuser3@example.com",
        "password": "password3",
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["access_token"], str)

    cookies = response.cookies
    assert "refresh_token" in cookies


async def test_login(client: TestClient):
    data = {
        "email": "testuser3@example.com",
        "password": "password3",
    }
    response = await client.post("/auth/login", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["access_token"], str)

    cookies = response.cookies
    assert "refresh_token" in cookies


async def test_logout(client: TestClient):
    data = {
        "email": "testuser3@example.com",
        "password": "password3",
    }
    response = await client.post("/auth/login", json=data)
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/auth/logout")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Logged out successfully"}

    cookies = response.cookies
    assert "refresh_token" not in cookies
