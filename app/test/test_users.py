import json
import pytest


@pytest.mark.asyncio
async def test_create_user_health_professional(test_app):
    test_data = {
        "full_name": "Diego Pardo Utest",
        "phone_number": "+57 3223456783",
        "address": "calle 1234",
        "gender": "M",
        "birthdate": "1999-01-23",
        "height": {
            "val": 1.79,
            "unit": "m"
        },
        "weight": {
            "val": 88,
            "unit": "Kg"
        },
        "user_type": 2
    }

    response = test_app.post("/users/", data=json.dumps(test_data),)
    res_json = response.json()

    assert response.status_code == 201
    assert 'created_at' in res_json
    assert res_json.get('health_info') is None
    assert res_json.get('age') == 23
    assert res_json.get('imc') == 27.46

    for key, value in test_data.items():
        assert value == res_json[key]


@pytest.mark.asyncio
async def test_create_user_normal(test_app):
    test_data = {
        "full_name": "Diego Pardo Utest",
        "phone_number": "+57 3223456783",
        "address": "calle 1234",
        "gender": "M",
        "birthdate": "1999-01-23",
        "height": {
            "val": 1.79,
            "unit": "m"
        },
        "weight": {
            "val": 88,
            "unit": "Kg"
        },
        "user_type": 1,
        "health_info": {
            "medicine": "N",
            "smoke": "Y",
            "heartAttack": "N",
            "thrombosis": "NK",
            "nephropathy": "N"
        }
    }

    response = test_app.post("/users/", data=json.dumps(test_data),)
    res_json = response.json()

    assert response.status_code == 201
    assert 'created_at' in res_json
    assert res_json.get('age') == 23
    assert res_json.get('imc') == 27.46

    for key, value in test_data.items():
        assert value == res_json[key]

@pytest.mark.asyncio
async def test_create_user_health_validation(test_app):
    test_data = {
        "full_name": "Diego Pardo Utest",
        "phone_number": "+57 3223456783",
        "address": "calle 1234",
        "gender": "M",
        "birthdate": "1999-01-23",
        "height": {
            "val": 1.79,
            "unit": "m"
        },
        "weight": {
            "val": 88,
            "unit": "Kg"
        },
        "user_type": 1
    }

    response = test_app.post("/users/", data=json.dumps(test_data),)
    res_json = response.json()

    assert response.status_code == 422
    assert res_json['detail'][0]['msg'] == 'health_info is required'

