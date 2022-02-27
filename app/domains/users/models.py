from datetime import datetime, date
from typing import Optional
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, PositiveFloat
from ...core.baseModel import CoreModelMixin, IDModelMixin
from .enums import SIsystemUnitEnum, HealthInfoEnum, GenderEnum, UserTypeEnum



class UnitModel(BaseModel):
    val: float | int
    unit: SIsystemUnitEnum


class HealthInfoModel(BaseModel):
    medicine: HealthInfoEnum
    smoke: HealthInfoEnum
    heartAttack: HealthInfoEnum
    thrombosis: HealthInfoEnum
    nephropathy: HealthInfoEnum

class UserModel(BaseModel):
    full_name: str
    phone_number: str
    address: str
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    gender: GenderEnum
    birthdate: date
    height: UnitModel
    weight: UnitModel
    user_type: UserTypeEnum
    health_info: Optional[HealthInfoModel]
    profile_url: Optional[str]

class UserCreate(CoreModelMixin, IDModelMixin, UserModel):
    age: Optional[int]
    imc: Optional[PositiveFloat]

    def calculate_age(self):
        time_difference = relativedelta(datetime.utcnow(), self.birthdate)
        self.age = time_difference.years

    def calculate_IMC(self):
        # TODO use unit for calculate IMC in accordance to system unit
        self.imc = round(self.weight.val / self.height.val**2, 2)

    def calculate_vars(self):
        self.calculate_age()
        self.calculate_IMC()


class UserUpdate(BaseModel):
    phone_number: Optional[str]
    address: Optional[str]
    location: Optional[str]
    height: Optional[UnitModel]
    weight: Optional[UnitModel]
    profile_url: Optional[str]


class UserInDB(CoreModelMixin, IDModelMixin):
    full_name: str
    phone_number: str
    address: str
    gender: str
    birthdate: str
    height: UnitModel
    weight: UnitModel
    user_type: str


class UserPublic(IDModelMixin, UserModel):
    age: Optional[int]
    imc: Optional[PositiveFloat]
    pass
