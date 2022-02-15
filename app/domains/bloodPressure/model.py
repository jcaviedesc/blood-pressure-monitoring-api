from dataclasses import field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class BPMeasurementModel(BaseModel):
    sys: int = Field(..., gt=0)
    dia: int = Field(..., gt=0)
    bpm: Optional[int] = Field(..., gt=0)
    datetime: datetime = Field(...)
    why: Optional[str]
    


class BPrecordModel(BaseModel):
    user_id: str
    records: list[BPMeasurementModel] = Field(..., min_items=1, max_items=2)
    sys_average: float
    dia_average: float
    timestamp: Optional[datetime]  # day/month/year
