from typing import Optional
from enum import Enum
from pydantic import BaseModel, validator, Field


class GenderEnum(str, Enum):
    male = "M"
    female = "F"


class SIsystemUnitEnum(str, Enum):
    second = "s"
    metre = "m"
    kilogram = "Kg"


class UserTypeEnum(str, Enum):
    healt = "health professional"
    normal = "normal"


class HealthInfoEnum(str, Enum):
    yes = "Y"
    no = "N"
    not_know = "NK"


class UnitModel(BaseModel):
    val: int | float
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
    birthdata: str
    height: UnitModel
    weight: UnitModel
    user_type: UserTypeEnum
    healt_info: Optional[HealthInfoModel]
    profile_url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Diego Pardo",
                "phone_number": "+57 3223456783",
                "address": "calle 1234",
                "gender": "M",
                "birthdata": "09/01/1999",
                "height": {
                    "val": 1.80,
                    "unit": "m"
                },
                "weight": {
                    "val": 70,
                    "unit": "Kg"
                },
                "user_type": "health professional",
            }
        }
