import pytest
from app.domains.blood_pressure.repository import BPRepository

@pytest.mark.asyncio
async def test_list_bp_records(test_app):
    print(test_app.request)
    test_data = {"id": 1, "title": "something", "description": "something else"}

    # async def mock_get(id):
    #     return test_data

    # monkeypatch.setattr(BPRepository, "get_records", mock_get)
    response = await test_app.get("/blood-pressure/user/2?interval=day&start_date=2022-2-14")
    assert response.status_code == 200
    assert response.json() == test_data