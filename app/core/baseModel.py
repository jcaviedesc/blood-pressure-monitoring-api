import datetime
import uuid
from pydantic import BaseModel, validator, Field


class CoreModelMixin(BaseModel):
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @validator("created_at", "updated_at", pre=True, always=True)
    def default_datetime(
        cls,  # noqa: N805
        value: datetime.datetime,  # noqa: WPS110
    ) -> datetime.datetime:
        return datetime.datetime.utcnow()

class IDModelMixin(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True
