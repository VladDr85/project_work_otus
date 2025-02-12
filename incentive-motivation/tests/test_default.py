import pytest
from httpx import AsyncClient, ASGITransport
from main import main_app

from api.api_v1.incentive_list import IncentiveList


def test_one():
    res = 1
    assert res == 1


@pytest.mark.asyncio
async def test_get_incentive_lists():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/incentive_lists/")
        data = response.json()
        assert response.status_code == 401
        assert data["detail"] == "Unauthorized"
