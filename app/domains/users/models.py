from datetime import datetime, date
from typing import Optional
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, PositiveFloat, HttpUrl
from ...core.baseModel import DatatimeModelMixin, IDModelMixin
from .schemas import  UnitModel, UserBaseSchema, HealthQuestionsModel
from .enums import GenderEnum, HealthInfoEnum, AsystemUnitEnum, CardiovascularRiskOption, UserTypeEnum


class UserCreateBase(IDModelMixin, DatatimeModelMixin, UserBaseSchema):
    age: Optional[int]
    imc: Optional[PositiveFloat]
    
    def calculate_age(self):
        time_difference = relativedelta(datetime.utcnow(), self.birthdate)
        self.age = time_difference.years
        return self

    def calculate_IMC(self):
        # TODO use unit for calculate IMC in accordance to system unit
        # Fórmula: peso (kg) / [estatura (m)]2
        height = self.height.val
        if self.height.unit == AsystemUnitEnum.centimeter:
            height = self.height.val / 100
        self.imc = round(self.weight.val / height**2, 2)
        return self


class PatientUserCreate(UserCreateBase):
    health_questions: HealthQuestionsModel = Field(..., alias="questions")
    role: int = Field(UserTypeEnum.patient, const=True)
    cardiovascular_risk: Optional[CardiovascularRiskOption] = Field(None, alias='cardiovascular_risk')

    def set_cardiovascular_risk(self):
        if HealthInfoEnum.yes in self.health_questions.dict().values():
            self.cardiovascular_risk = CardiovascularRiskOption.HIGHT
        else:
            self.cardiovascular_risk = CardiovascularRiskOption.LOW

class ProfessionalUserCreate(UserCreateBase):
    avatar: HttpUrl = Field(...)
    role: int = Field(UserTypeEnum.health_professional, const=True)

class UserCreatedModel(UserCreateBase):
    cardiovascular_risk: Optional[CardiovascularRiskOption]
    pass

class UserUpdate(BaseModel):
    phone: Optional[str]
    address: Optional[str]
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    gender: Optional[GenderEnum]
    birthdate: Optional[date]
    height: Optional[UnitModel]
    weight: Optional[UnitModel]
    profile_url: Optional[str]
