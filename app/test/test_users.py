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


@pytest.mark.asyncio
async def test_find_user(test_app):
    test_data_result = {
        "full_name": "Diego Pardo",
        "phone_number": "+573223456783",
        "address": "calle 1234",
        "gender": "M",
        "birthdate": "1999-02-23",
        "height": {
            "val": 1.8,
            "unit": "m"
        },
        "weight": {
            "val": 70,
            "unit": "Kg"
        },
        "user_type": 2,
        "id": "72f3d6cf-63bb-478c-809b-d9a73446ebb8",
        "age": 23,
        "imc": 21.6
    }
    response = test_app.get(
        "/users?phone=%2B573223456783")
    assert response.status_code == 200
    assert response.json() == test_data_result

@pytest.mark.asyncio
async def test_find_user_not_found(test_app):
    phone = '+570000000'
    response = test_app.get(
        "/users/%2B570000000")
    assert response.status_code == 404
    print(response.json())
    assert response.json().get('msg') == 'user with phone_number {} not found'.format(phone)

