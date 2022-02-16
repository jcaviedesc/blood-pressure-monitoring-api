from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED
from fastapi.encoders import jsonable_encoder
from app.dependencies.database import get_repository
from .repository import BloodPressureRepository
from .models import InsertBpRecordModel, BloodPressureSchema


router = APIRouter(prefix="/blood-pressure", tags=["Blood pressure"])


@router.post("/", response_model=InsertBpRecordModel, status_code=HTTP_201_CREATED)
async def create_bp_record(
    BPrecord: BloodPressureSchema = Body(...),
    bp_repo: BloodPressureRepository = Depends(get_repository(BloodPressureRepository))
) -> BloodPressureSchema:
    created_BPrecord = await bp_repo.insert(new_record=BPrecord)
    return JSONResponse(status_code=HTTP_201_CREATED, content=jsonable_encoder(created_BPrecord, exclude_defaults=True))

