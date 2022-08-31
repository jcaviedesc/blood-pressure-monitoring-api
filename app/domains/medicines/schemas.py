from enum import Enum
from datetime import time
from pydantic import BaseModel, Field
from typing import Literal, Optional


DAYS = Literal['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
APPARIENCE = Literal['pill', 'solution',
                     'injection', 'dust', 'drops', 'inhaler', 'other']
DOSE_UNITS = Literal['g','IU','mcg','mcg/hr','mcg/ml','mEq','mg','mg/cm2','mg/g','mg/ml','mL','%']
class DoseSchema(BaseModel):
    unit: DOSE_UNITS = Field(..., alias='u')
    value: int = Field(..., alias='v')

    class Config:
        allow_population_by_field_name = True


class FrecuencyEnum(str, Enum):
    EVERY_DAY = 'every day'
    SPECIFIC_DAYS = 'specific days'
    DAYS_INTERVAL = 'days interval'
class MedicinesSchema(BaseModel):
    name: str = Field(..., min_length=3)
    apparience: APPARIENCE = Field(...)
    dose: DoseSchema = Field(...)
    via: str = Field(...)
    frecuency: FrecuencyEnum = Field(...)
    times_per_day: int = Field(..., ge=1, le=24,
                               description='Numero de veces que se toma la medicina en un dia')
    days: Optional[list[DAYS]] = Field(
        None, max_items=7, min_items=1, description='Listado de dias de la semana, Esta opcion es requerida cuando frecuency es igual a SPECIFIC_DAYS')
    # esta opcion es requerida cuando frecuency es DAYS_INTERVAL
    every: Optional[int] = Field(
        None, ge=1, description='Numero que representa el ciclo en dias, esta opcion es requerida cuando frecuency es DAYS_INTERVAL')
    times: list[time] = Field(..., min_items=1,
                              description='Hora y minuto a la que se toma la medicina')

# TODO add validations
