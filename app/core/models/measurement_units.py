
from pydantic import BaseModel, Field
from ..enums import SIsystemUnitEnum, AsystemUnitEnum

class UnitModel(BaseModel):
    val: float | int = Field(..., alias="v")
    unit: SIsystemUnitEnum | AsystemUnitEnum = Field(..., alias="u")

    class Config:
        allow_population_by_field_name = True