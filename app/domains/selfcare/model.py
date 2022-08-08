from pydantic import Field
from .schema import SelfcareTipSchema;
from ...core.baseModel import DatatimeModelMixin, IDModelMixin, OwnerMixin

class SelfcareModel(SelfcareTipSchema, DatatimeModelMixin, IDModelMixin, OwnerMixin):
    title: str = Field(...)
    class Config:
        allow_population_by_field_name = True

class SelfcareReturnInsertModel(SelfcareTipSchema, IDModelMixin):
    pass

class SelfcarePublicModel(SelfcareTipSchema, IDModelMixin, OwnerMixin):
    pass