from pydantic import Field
from .schema import SelfcareTipSchema;
from ...core.baseModel import DatetimeModelMixin, IDModelMixin, OwnerMixin

class SelfcareModel(SelfcareTipSchema, DatetimeModelMixin, IDModelMixin, OwnerMixin):
    title: str = Field(...)
    class Config:
        allow_population_by_field_name = True

class SelfcareReturnInsertModel(SelfcareTipSchema, IDModelMixin):
    pass

class SelfcarePublicModel(SelfcareTipSchema, IDModelMixin, OwnerMixin):
    pass