from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, HttpUrl
from .enums import GenderEnum, UserTypeEnum, SIsystemUnitEnum, AsystemUnitEnum, HealthInfoEnum


class UnitModel(BaseModel):
    val: float | int = Field(..., alias="v")
    unit: SIsystemUnitEnum | AsystemUnitEnum = Field(..., alias="u")

    class Config:
        allow_population_by_field_name = True


class HealthQuestionsModel(BaseModel):
    medicine: HealthInfoEnum = Field(..., alias="med")
    smoke: HealthInfoEnum = Field(..., alias="smo")
    heart_attack: HealthInfoEnum = Field(..., alias="heaAtt")
    thrombosis: HealthInfoEnum = Field(..., alias="thr")
    nephropathy: HealthInfoEnum = Field(..., alias="nep")

    class Config:
        allow_population_by_field_name = True


class UserBaseSchema(BaseModel):
    name: str = Field(...)
    last_name: str = Field(..., alias="lname")
    doc_id: str = Field(...)
    phone: str = Field(...)
    address: str
    location: Optional[list[int]] = Field(None, max_items=2, min_items=2)
    sex: GenderEnum = Field(...)
    birthdate: date = Field(...)
    height: UnitModel = Field(...)
    weight: UnitModel = Field(...)
    profession: Optional[str]
    occupation: str = Field(None, min_length=3)
    role: UserTypeEnum = Field(...)
    avatar: Optional[HttpUrl] = Field(None, alias="avatar")
    health_questions: HealthQuestionsModel = Field(..., alias="questions")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Estefani",
                "last_name": "Salas",
                "doc_id": "12444514",
                "phone": "+57 3223456783",
                "address": "calle 1234",
                "sex": "M",
                "birthdate": "1999-01-23",
                "height": {
                    "val": 1.80,
                    "unit": "m"
                },
                "weight": {
                    "val": 70,
                    "unit": "Kg"
                },
                "role": 2,  # role 2 igual a paciente
                "questions": {
                    "medicine": "Y",
                    "smoke": "N",
                    "heart_attack": "N",
                    "thrombosis": "N",
                    "nephropathy": "N"
                }
            }
        }


class PatientUserSchema(UserBaseSchema):
    health_questions: HealthQuestionsModel = Field(..., alias="questions")
    role: int = Field(UserTypeEnum.patient, const=True)


class ProfesionalUserSchema(UserBaseSchema):
    avatar: HttpUrl = Field(...)
    role: int = Field(UserTypeEnum.health_professional, const=True)
