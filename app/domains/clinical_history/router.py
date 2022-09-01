from fastapi import APIRouter, Body, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette import status
from fastapi.encoders import jsonable_encoder
from firebase_admin import auth
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from app.domains.users.enums import UserTypeEnum
from ...dependencies.database import get_repository
from ...dependencies.authorization import get_user, get_user_with_claims, get_professional_user
from ...core.enums import PageLimitEnum

router = APIRouter(prefix='/clincal-history', tags=['Clinical history'])

@router.patch("/{patient_id}", status_code=status.HTTP_201_CREATED)
async def request_access_to_medical_records(patient_id: str, auth_professional_user=Depends(get_professional_user)):
    pass