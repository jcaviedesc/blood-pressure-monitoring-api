from datetime import datetime, date
from typing import Optional
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, PositiveFloat, HttpUrl, PositiveInt
from ...core.baseModel import DatetimeModelMixin, IDModelMixin
from ..models.measurement_units import UnitModel
from ..enums import GenderEnum, HealthInfoEnum, AsystemUnitEnum, CardiovascularRiskOption, UserTypeEnum


class UserMeasurementModel(BaseModel):
    name: str
    value: float | str = Field(..., alias="v")
    unit: str = Field(..., alias="u")
    last_measurement: datetime | str = Field(..., alias="lst_msrmnt")
    status: str
    category: str

    class Config:
        allow_population_by_field_name = True


class UserCreateBase(IDModelMixin, DatetimeModelMixin):
    name: str = Field(...)
    last_name: str = Field(...)
    doc_id: str = Field(...)
    phone: str = Field(...)
    address: Optional[str]
    birthdate: date = Field(...)
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    sex: GenderEnum = Field(...)
    role: UserTypeEnum = Field(...)
    profession: Optional[str]
    occupation: Optional[str] = Field(None, min_length=3)
    avatar: Optional[HttpUrl] = Field(None)
    age: Optional[PositiveInt]
    bmi: Optional[PositiveFloat]
    measurements: Optional[list[UserMeasurementModel]]

    def calculate_age(self):
        time_difference = relativedelta(datetime.utcnow(), self.birthdate)
        self.age = time_difference.years
        return self

    def calculate_body_mass_index(self, height: UnitModel, weight: UnitModel):
        # TODO use unit for calculate IMC in accordance to system unit
        # Fórmula: peso (kg) / [estatura (m)]2
        bmi_height = height.val
        if height.unit == AsystemUnitEnum.centimeter:
            bmi_height = height.val / 100
        self.bmi = round(weight.val / bmi_height**2, 2)
        return self

    def set_initial_measurements(self, height: UnitModel, weight: UnitModel):
        timestamp = datetime.utcnow()
        height_measurement = UserMeasurementModel(
            name="Height", v=height.val, u=height.unit, lst_msrmnt=timestamp, status="normal", category='Body')
        weight_measurement = UserMeasurementModel(
            name="Weight", v=weight.val, u=weight.unit, lst_msrmnt=timestamp, status="normal", category='Body')
        blood_pressure = UserMeasurementModel(
            name="BloodPressure", v=0, u="mmHg", lst_msrmnt="", status="no data", category='Heart')

        self.measurements = [blood_pressure, height_measurement,
                             weight_measurement]


class PatientUserCreate(UserCreateBase):
    role: int = Field(UserTypeEnum.patient, const=True)
    cardiovascular_risk: Optional[CardiovascularRiskOption]

    def set_cardiovascular_risk(self, health_questions: dict):
        if HealthInfoEnum.yes in health_questions.values():
            self.cardiovascular_risk = CardiovascularRiskOption.HIGHT
        else:
            self.cardiovascular_risk = CardiovascularRiskOption.LOW


class ProfessionalUserCreate(UserCreateBase):
    avatar: HttpUrl = Field(...)
    role: int = Field(UserTypeEnum.health_professional, const=True)


class UserCreatedModel(UserCreateBase):
    cardiovascular_risk: Optional[CardiovascularRiskOption]
    linked_professionals: Optional[list[str]] = []
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


class UserUpdateLinkedProfessionals(IDModelMixin):
    linked_professionals: list[str]
