from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field, PositiveFloat
from app.core.baseModel import IDModelMixin


class BPMeasurementModel(BaseModel):
    sys: int = Field(..., gt=0)
    dia: int = Field(..., gt=0)
    bpm: Optional[int]
    datetime: datetime


class BPrecordModel(IDModelMixin):
    user_id: str
    records: list[BPMeasurementModel] = Field(..., min_items=1, max_items=2)
    sys_avg: Optional[PositiveFloat]
    dia_avg: Optional[PositiveFloat]
    timestamp: Optional[datetime]  # day/month/year
    why: Optional[str]
