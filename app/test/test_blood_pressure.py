import pytest

@pytest.mark.asyncio
async def test_list_bp_records(test_app):
    test_data = {
        "records": [
            {
                "sys": 120,
                "dia": 90,
                "bpm": 5,
                "datetime": "20:19:17"
            },
            {
                "sys": 125,
                "dia": 91,
                "bpm": 5,
                "datetime": "20:22:17"
            },
            {
                "sys": 120,
                "dia": 90,
                "bpm": 5,
                "datetime": "20:19:17"
            },
            {
                "sys": 125,
                "dia": 91,
                "bpm": 5,
                "datetime": "20:22:17"
            }
        ],
        "sys": 122.5,
        "dia": 90.5,
        "bpm": 5,
        "interval": "day"
    }

    response = test_app.get(
        "/blood-pressure/user/2?interval=day&start_date=2022-2-14")
    assert response.status_code == 200
    assert response.json() == test_data
