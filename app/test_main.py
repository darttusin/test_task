from app.main import app
from fastapi.testclient import TestClient
import asyncio
import pytest


client = TestClient(app)


@pytest.mark.asyncio
async def test_init():
    responce = client.get("/initialize")
    assert responce.status_code == 200
    assert responce.json() == {"detail": "successful"}
