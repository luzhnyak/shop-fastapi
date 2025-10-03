from fastapi.testclient import TestClient
from fastapi import status


async def test_postgres(client: TestClient):
    response = await client.get("/test_postgres")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Postgres connection test successful"
