from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, validator, Field, PositiveFloat
from app.core.baseModel import IDModelMixin


class IntervalEnum(str, Enum):
    day = "day"
    week = "week"


class BPRecordModel(BaseModel):
    sys: int = Field(..., gt=0)
    dia: int = Field(..., gt=0)
    bpm: Optional[int]
    datetime: datetime | str

    def parse_datetime_to_time(self):
        self.datetime = self.datetime.strftime("%X")
        return self


class BPSchema(BaseModel):
    user_id: str
    records: list[BPRecordModel] = Field(..., min_items=1, max_items=2)
    why: Optional[str]
    datetime: datetime | str
    location: list[float] = Field(..., min_items=2, max_items=2)


class BPRecordsModel(BPSchema):
    user_id: Optional[str]
    location: Optional[list[float]]

    def parse_datetime_to_day(self):
        self.datetime = self.datetime.strftime("%Y-%m-%d")
        self.records = [record.parse_datetime_to_time()
                        for record in self.records]


def sum_records(key: str, records: list[BPRecordModel]) -> int:
    return sum(list(map(lambda record: record.dict().get(key), records)))


class InsertBpRecordModel(IDModelMixin,BPSchema):
    sys_avg: Optional[PositiveFloat]
    dia_avg: Optional[PositiveFloat]
    timestamp: Optional[datetime]  # day/month/year

    @validator("timestamp", pre=True, always=True)
    def default_datetime(cls, value: int) -> datetime:
        return datetime.utcnow()

    def calculate_avg(self) -> None:
        total_records = len(self.records)
        self.sys_avg = float(sum_records("sys", self.records) / total_records)
        self.dia_avg = float(sum_records("dia", self.records) / total_records)

class BPRecordResponseModel(BaseModel):
    records: list[BPRecordModel]
    sys: PositiveFloat
    dia: PositiveFloat
    bpm: PositiveFloat
    interval: IntervalEnum
