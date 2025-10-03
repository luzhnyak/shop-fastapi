from fastapi.testclient import TestClient
from fastapi import status


async def test_redis(client: TestClient):
    response = await client.get("/test_redis")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Redis connection test successful"
