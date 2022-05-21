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


@pytest.mark.asyncio
async def test_search_blood_pressure_monitor(test_app):
    test_data = [
        {
            "brand": "A&D",
            "model": "UM-201",
            "measurement_site ": "Brazo",
            "use": "Casa",
            "validation_study": "Adultos",
            "img": "https://www.stridebp.org/images/devices/16/1557218787.0396.jpg",
            "measurement_method": "Oscilométrico automatizado",
            "additional": None
        },
        {
            "brand": "A&D",
            "model": "UM-211",
            "measurement_site ": "Brazo",
            "use": "Consultorio/Clínica, Hospital",
            "validation_study": "Adultos",
            "img": "https://www.stridebp.org/images/devices/260/1561022634.5825.jpg",
            "measurement_method": "Automated oscillometric, Hybrid manual auscultatory",
            "additional": "Automated storage of multiple readings"
        }
    ]
    search = 'UM-2'

    response = test_app.get(
        f'/blood-pressure/monitors?q={search}')
    assert response.status_code == 200
    assert response.json() == test_data
