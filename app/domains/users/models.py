from typing import Optional
from pydantic import BaseModel
from .schemas import UserSchema, UnitModel
from app.core.baseModel import CoreModelMixin, IDModelMixin


class UserCreate(CoreModelMixin, IDModelMixin, UserSchema):
    pass


class UserUpdate(BaseModel):
    phone_number: str
    address: str
    location: Optional[str]
    weight: UnitModel
    profile_url: Optional[str]


class UserPublic(IDModelMixin, UserSchema):
    pass
