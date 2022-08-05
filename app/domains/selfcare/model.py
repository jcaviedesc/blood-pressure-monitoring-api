from pydantic import BaseModel
from .schema import SelfcareTipSchema;
from ...core.baseModel import DatatimeModelMixin, IDModelMixin, OwnerMixin

class SelfcareModel(SelfcareTipSchema, DatatimeModelMixin, IDModelMixin, OwnerMixin):
    class Config:
        allow_population_by_field_name = True
