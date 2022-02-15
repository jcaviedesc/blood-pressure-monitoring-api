from typing import Optional, Dict
from dateutil.relativedelta import relativedelta
import datetime
from pydantic import BaseModel, validator
from .schemas import UserSchema, UnitModel
from app.core.baseModel import CoreModelMixin, IDModelMixin


class UserCreate(CoreModelMixin, IDModelMixin, UserSchema):
    age: Optional[int]

    @validator("age", always=True)
    def calculate_age(cls, value: int, values: Dict) -> int:
        [day, month, year] = values["birthdate"].split("/")
        time_difference = relativedelta(datetime.datetime.utcnow(
        ), datetime.datetime(day=int(day), month=int(month), year=int(year)))
        difference_in_years = time_difference.years
        return difference_in_years


class UserUpdate(BaseModel):
    phone_number: str
    address: str
    location: Optional[str]
    weight: UnitModel
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


class UserPublic(IDModelMixin, UserSchema):
    pass
