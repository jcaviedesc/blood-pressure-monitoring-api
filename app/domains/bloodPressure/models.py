from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, validator, Field, PositiveFloat
from app.core.baseModel import IDModelMixin


class BPMeasurementModel(BaseModel):
    sys: int = Field(..., gt=0)
    dia: int = Field(..., gt=0)
    bpm: Optional[int]
    datetime: datetime


class BloodPressureSchema(BaseModel):
    user_id: str
    records: list[BPMeasurementModel] = Field(..., min_items=1, max_items=2)
    why: Optional[str]
    datetime: datetime
    location: list[float] = Field(...,min_items=2, max_items=2)

def sumRecords(key: str, records: list[BPMeasurementModel]) -> int:
    return sum(list(map(lambda record: record.dict().get(key), records)))

class InsertBpRecordModel(IDModelMixin, BloodPressureSchema):
    sys_avg: Optional[PositiveFloat]
    dia_avg: Optional[PositiveFloat]
    timestamp: Optional[datetime]  # day/month/year

    @validator("timestamp", pre=True, always=True)
    def default_datetime(cls, value: int) -> datetime:
        return datetime.utcnow()

    def calculate_avg(self) -> None:
        total_records = len(self.records)
        self.sys_avg = float(sumRecords("sys", self.records) / total_records)
        self.dia_avg = float(sumRecords("dia", self.records) / total_records)


class BpRecordModel(BaseModel):
    records: list[BPMeasurementModel]
    sys_avg: Optional[PositiveFloat]
    dia_avg: Optional[PositiveFloat]
    interval: str
