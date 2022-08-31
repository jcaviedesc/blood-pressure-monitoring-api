from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from starlette import status
from fastapi.encoders import jsonable_encoder


from ...dependencies.database import get_repository
from ...dependencies.authorization import get_user_with_claims
from .schemas import MedicinesSchema
from .examples.post import examples
from .repository import MedicineRepository
from .models import MedicineModelCreate

router = APIRouter(prefix='/medicines', tags=['Medicines'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_medicine(
    new_medicine: MedicinesSchema = Body(..., examples=examples),
    auth_user=Depends(get_user_with_claims),
    medicine_repo: MedicineRepository = Depends(
        get_repository(MedicineRepository))
):
    medicine = MedicineModelCreate(**new_medicine.dict())
    user_id = auth_user.custom_claims.get('ref')
    medicine.set_user_id(user_id)

    medicine_added = await medicine_repo.add_medicine(medicine=medicine)
    if not medicine_added is None:
        return JSONResponse(content=jsonable_encoder(medicine_added, exclude_defaults=True, by_alias=False), status_code=status.HTTP_201_CREATED)

# TODO add response model
@router.get('', status_code=status.HTTP_200_OK, response_model=list[MedicineModelCreate])
async def list_medicines(auth_user=Depends(get_user_with_claims),medicine_repo: MedicineRepository = Depends(get_repository(MedicineRepository))):
    user_id = auth_user.custom_claims.get('ref')
    medicines = await medicine_repo.list_medicines(user_id=user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            medicines, exclude_defaults=True, by_alias=False)
    )