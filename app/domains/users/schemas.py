from typing import Dict
from pydantic import validator
from .models import UserModel, UserTypeEnum


class UserSchema(UserModel):

    @validator("health_info", always=True)
    def validate_health_info(cls, value, values: Dict):
        if values["user_type"] == UserTypeEnum.health_professional and value is None:
            raise ValueError("health_info is required")
        return value

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Diego Pardo",
                "phone_number": "+57 3223456783",
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
