from typing import Dict
from pydantic import validator
from .models import UserModel, UserTypeEnum, InitialUserCreateModel


class InitialUserSchema(InitialUserCreateModel):
    class Config:
        schema_extra = {
            "example": {
                "full_name": "Diego Pardo",
                "doc_id": "12444514",
                "phone": "+573223456783",
            }
        }


class UserSchema(UserModel):
    @validator("health_info", always=True)
    def validate_health_info(cls, value, values: Dict):
        if values.get('user_type', -1) == UserTypeEnum.patient and value is None:
            raise ValueError("health_info is required")
        return value

    class Config:
        schema_extra = {
            "example": {
                "address": "calle 1234",
                "gender": "M",
                "birthdate": "1999-01-23",
                "height": {
                    "val": 1.80,
                    "unit": "m"
                },
                "weight": {
                    "val": 70,
                    "unit": "Kg"
                },
                "user_type": 1,
            }
        }
