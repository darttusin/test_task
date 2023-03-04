from app import app
from fastapi.testclient import TestClient
import pytest


client: TestClient = TestClient(app)


@pytest.mark.asyncio
async def test_init() -> None:
    responce = client.get("/initialize")
    assert responce.status_code == 200
    assert responce.json() == {"detail": "successful"}


@pytest.mark.asyncio
async def test_search() -> None:
    responce = client.get("/find=mercedes")
    assert responce.status_code == 200
