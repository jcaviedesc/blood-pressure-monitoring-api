from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, validator, Field


class DatetimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        None, alias="ctd_at")  # type: ignore
    updated_at: Optional[datetime] = Field(
        None, alias="utd_at")  # type: ignore

    @validator("created_at", "updated_at", pre=True, always=True)
    def default_datetime(cls, value: int) -> datetime:
        # TODO quisa aqui podemos agregar una validacion y si
        # created_at y updated_at son fechas validad y menores a now aceptar el valor
        return datetime.utcnow()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class IDModelMixin(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(BaseModel):
    name: str
    avatar: str
    id: PyObjectId = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class OwnerMixin(BaseModel):
    owner: Optional[User]

    def add_user(self, user: User):
        self.owner = user
