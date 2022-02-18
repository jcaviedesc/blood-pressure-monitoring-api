from datetime import date, timedelta
from ...db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import InsertBpRecordModel, BPSchema, IntervalEnum, BPRecordsModel


class BPRepository(BaseRepository):
    """"
    All database actions associated with the Blood-pressure resource
    """
    async def insert(self, *, new_record: BPSchema) -> BPSchema:
        wrapper_record = InsertBpRecordModel(**new_record.dict())
        wrapper_record.calculate_avg()
        record_encoder = jsonable_encoder(
            wrapper_record, exclude_defaults=True)
        created_record = await self.db.bp_records.insert_one(record_encoder)
        record = await self.db.bp_records.find_one({"_id": created_record.inserted_id})
        return BPSchema(**record)

    async def get_records(
        self,
        *,
        user_id: str,
        start_date: date,
        interval: IntervalEnum,
        fields: list[str] | None = None
    ) -> list[BPRecordsModel]:
        end_days = 7 if interval == IntervalEnum.week else 1
        end_date = start_date + timedelta(days=end_days)
        query = {
            "user_id": user_id,
            "datetime": {
                "$gte": start_date.isoformat(),
                "$lt": end_date.isoformat()
            }
        }

        projection = {
            "records": 1,
            "why": 1,
            "datetime": 1
        }
        if fields is not None:
            projection = {k: 1 for k in fields}

        records = []
        for record in await self.db.bp_records.find(query, projection).to_list(length=100):
            parse_record = BPRecordsModel(**record)
            parse_record.parse_datetime_to_day()
            records.append(parse_record)

        return records
