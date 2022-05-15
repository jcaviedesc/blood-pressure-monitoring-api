from datetime import datetime, date
from typing import Optional
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, PositiveFloat, HttpUrl
from ...core.baseModel import DatatimeModelMixin, IDModelMixin
from .enums import SIsystemUnitEnum, HealthInfoEnum, GenderEnum, UserTypeEnum, AsystemUnitEnum


class InitialUserCreateModel(BaseModel):
    full_name: str = Field(..., alias="fName")
    # documento de identificación ej cedula de ciudadania
    doc_id: str = Field(..., alias="docId")
    phone: str

    class Config:
        allow_population_by_field_name = True

#TODO revisar porque no devuelve is_complete?
class IntitalUserCreate(InitialUserCreateModel, DatatimeModelMixin, IDModelMixin):
    is_complete: Optional[bool] = Field(default=False, alias="isC")


class UnitModel(BaseModel):
    val: float | int = Field(..., alias="v")
    unit: SIsystemUnitEnum | AsystemUnitEnum = Field(..., alias="u")

    class Config:
        allow_population_by_field_name = True


class HealthInfoModel(BaseModel):
    medicine: HealthInfoEnum = Field(..., alias="med")
    smoke: HealthInfoEnum = Field(..., alias="smo")
    heart_attack: HealthInfoEnum = Field(..., alias="heaAtt")
    thrombosis: HealthInfoEnum = Field(..., alias="thr")
    nephropathy: HealthInfoEnum = Field(..., alias="nep")

    class Config:
        allow_population_by_field_name = True


class UserModel(BaseModel):
    address: str
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    gender: GenderEnum
    birthdate: date
    height: UnitModel
    weight: UnitModel
    user_type: UserTypeEnum = Field(..., alias="utype")
    health_info: Optional[HealthInfoModel] = Field(None, alias="healthI")
    avatar: Optional[HttpUrl] = Field(None, alias="avatar")

    class Config:
        allow_population_by_field_name = True
        extra = 'allow'


class UserCreate(UserModel):
    age: Optional[int]
    imc: Optional[PositiveFloat]

    def calculate_age(self):
        time_difference = relativedelta(datetime.utcnow(), self.birthdate)
        self.age = time_difference.years

    def calculate_IMC(self):
        # TODO use unit for calculate IMC in accordance to system unit
        # Fórmula: peso (kg) / [estatura (m)]2
        height = self.height.val
        if self.height.unit == AsystemUnitEnum.centimeter:
            height = self.height.val / 100
        self.imc = round(self.weight.val / height**2, 2)

    def calculate_vars(self):
        self.calculate_age()
        self.calculate_IMC()

    def set_is_complete(self):
        self.isC = True


class UserUpdate(BaseModel):
    phone: Optional[str]
    address: Optional[str]
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    gender: Optional[GenderEnum]
    birthdate: Optional[date]
    height: Optional[UnitModel]
    weight: Optional[UnitModel]
    profile_url: Optional[str]

class UserPublic(IDModelMixin, InitialUserCreateModel, UserCreate):
    pass
