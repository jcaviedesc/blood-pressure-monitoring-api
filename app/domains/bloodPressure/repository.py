from app.db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import BPrecordModel


class BloodPressureRepository(BaseRepository):
    """"
    All database actions associated with the Blood-pressure resource
    """
    async def insert(self, *, new_record: BPrecordModel) -> BPrecordModel:
        record_encoder = jsonable_encoder(new_record, exclude_defaults=True)
        created_record = await self.db.day_bp_records.insert_one(record_encoder)
        record = await self.db.day_bp_records.find_one({"_id": created_record.inserted_id})
        return BPrecordModel(**record)
