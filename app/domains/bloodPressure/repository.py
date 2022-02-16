from app.db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import InsertBpRecordModel, BloodPressureSchema


class BloodPressureRepository(BaseRepository):
    """"
    All database actions associated with the Blood-pressure resource
    """
    async def insert(self, *, new_record: BloodPressureSchema) -> BloodPressureSchema:
        wrapper_record = InsertBpRecordModel(**new_record.dict())
        wrapper_record.calculate_avg()
        record_encoder = jsonable_encoder(wrapper_record, exclude_defaults=True)
        created_record = await self.db.bp_records.insert_one(record_encoder)
        record = await self.db.bp_records.find_one({"_id": created_record.inserted_id})
        return BloodPressureSchema(**record)
