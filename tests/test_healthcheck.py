from fastapi.testclient import TestClient
from fastapi import status


async def test_healthcheck(client: TestClient):
    response = await client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
