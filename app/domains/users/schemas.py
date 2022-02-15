from typing import Optional, Dict
from enum import Enum, IntEnum
from pydantic import BaseModel, validator, Field


class GenderEnum(str, Enum):
    male = "M"
    female = "F"


class SIsystemUnitEnum(str, Enum):
    second = "s"
    metre = "m"
    kilogram = "Kg"


class UserTypeEnum(IntEnum):
    health_professional = 1
    normal = 2


class HealthInfoEnum(str, Enum):
    yes = "Y"
    no = "N"
    not_know = "NK"


class UnitModel(BaseModel):
    val: float | int
    unit: SIsystemUnitEnum


class HealthInfoModel(BaseModel):
    medicine: HealthInfoEnum
    smoke: HealthInfoEnum
    heartAttack: HealthInfoEnum
    thrombosis: HealthInfoEnum
    nephropathy: HealthInfoEnum


class UserSchema(BaseModel):
    full_name: str
    phone_number: str
    address: str
    location: Optional[str]
    gender: GenderEnum
    birthdate: str
    height: UnitModel
    weight: UnitModel
    user_type: UserTypeEnum
    health_info: Optional[HealthInfoModel]
    profile_url: Optional[str]

    @validator("health_info")
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
                "birthdate": "09/01/1999",
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
