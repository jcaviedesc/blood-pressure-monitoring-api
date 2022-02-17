from datetime import date
from functools import reduce
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from fastapi.encoders import jsonable_encoder
import pandas as pd
from app.dependencies.database import get_repository
from .repository import BPRepository
from .models import BPSchema, IntervalEnum, BPRecordResponseModel


router = APIRouter(prefix="/blood-pressure", tags=["Blood pressure"])


@router.post("/", response_model=BPSchema, status_code=HTTP_201_CREATED)
async def create_bp_record(
    BPrecord: BPSchema = Body(...),
    bp_repo: BPRepository = Depends(
        get_repository(BPRepository))
) -> BPSchema:
    created_BPrecord = await bp_repo.insert(new_record=BPrecord)
    return JSONResponse(status_code=HTTP_201_CREATED, content=jsonable_encoder(created_BPrecord, exclude_defaults=True))


@router.get("/user/{user_id}", response_model=list[BPRecordResponseModel], status_code=HTTP_201_CREATED)
async def list_bp_records(
    user_id: str,
    bp_repo: BPRepository = Depends(
        get_repository(BPRepository)),
    interval: IntervalEnum = IntervalEnum.day,
    start_date: date = date.today()
) -> BPRecordResponseModel:
    records_db = await bp_repo.get_records(user_id=user_id, start_date=start_date, interval=interval)
    result = {}
    if interval == IntervalEnum.day:
        records = sum([meassure.records for meassure in records_db], [])
        df_day = pd.DataFrame(jsonable_encoder(records, exclude_defaults=True))
        records_mean = df_day.mean().apply(lambda x: round(x, 2))
        result = BPRecordResponseModel(
            records=records, interval=interval, **records_mean)
    else:
        transform_data = map(lambda x: list(map(lambda y: {**y, "day": x.get("datetime")}, x.get(
            "records"))), jsonable_encoder(records_db, exclude_defaults=True))
        data = sum(list(transform_data), [])
        df_week = pd.DataFrame(data)
        df_week = df_week.groupby('day').mean()
        df_week["datetime"] = df_week.index

        records = df_week.to_dict('records')
        records_mean = dict(df_week.mean(
            numeric_only=True).apply(lambda x: round(x, 2)))

        result = BPRecordResponseModel(
            records=records, interval=interval, **records_mean)

    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(result, exclude_defaults=True))
