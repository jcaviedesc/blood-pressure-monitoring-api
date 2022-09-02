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
from .repository import UserRepository
from .schemas import UserBaseSchema
from .models import GenderEnum, PatientUserCreate, ProfessionalUserCreate


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=PatientUserCreate, status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: UserBaseSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    auth_user=Depends(get_user)
) -> JSONResponse:
    user = {}
    try:
        if new_user.role == UserTypeEnum.patient:
            questions = new_user.dict().get('health_questions', {})
            user = PatientUserCreate(**new_user.dict())
            user.set_cardiovascular_risk(questions)
        else:
            user = ProfessionalUserCreate(**new_user.dict())
    except ValidationError as err:
        raise RequestValidationError(errors=err.raw_errors)

    user.calculate_age()
    user.calculate_body_mass_index(height=new_user.height, weight=new_user.weight).set_initial_measurements(height=new_user.height, weight=new_user.weight)
    
    user_created = await users_repo.create_user(user=user)
    # TODO crear un servicio asyncrono que guarde las respuestas del usuario y no
    # consuma CPU y tiempo. Quisa con background task de fastapis

    if user_created:
        try:
            params = {
                "display_name": f'{user_created.name} {user_created.last_name}'
            }
            if (profile_url := user_created.avatar) is not None:
                params["photo_url"] = profile_url

            uid_user = auth_user.get('uid')
            auth.update_user(uid_user, **params)
            auth.set_custom_user_claims(
                uid_user, {"isRegistered": True, "ref": str(user_created.id), "role": user_created.role})

            logger.info("auth user {} updated".format(uid_user))
        except Exception as fba_err:
            logger.error(fba_err)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user_created, exclude_defaults=True, by_alias=False))
    else:
        user_already = f'User with phone {new_user.phone} already register'
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"msg": user_already})

# TODO cambiar
# @router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
# async def complete_create_user(
#     user_id: str,
#     user: PatientUserSchema = Body(...),
#     users_repo: UserRepository = Depends(get_repository(UserRepository)),
#     user_token=Depends(get_user)
# ):
#     user_complete = UserCreatePatient(**user.dict())
#     user_complete.calculate_age()
#     user_complete.calculate_IMC()
#     user_complete.finish_registration()
#     try:
#         user_updated = await users_repo.update_user(user=user_complete, user_id=user_id)
#     except Exception as db_error:
#         # TODO mejorar
#         logger.error(db_error)
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Sorry! we have some problems to process your request"})

#     if user_updated:
#         try:
#             params = {"display_name": user_updated.full_name, "disabled": False}
#             if (profile_url := user_updated.avatar) is not None:
#                 params["photo_url"] = profile_url
#             auth.update_user(user_token['uid'], **params)
#             auth.set_custom_user_claims(user_token['uid'], {'isC': True})
#         except ValueError as err:
#             # Panic send report for reprosed updated user
#             logger.info("There was a error updating user with ID {} in the auth provider".format(
#                 user_updated.id))
#             logger.error(err)

#         return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user_updated, exclude_defaults=True, by_alias=False))
#     else:
#         # TODO add i18-n
#         return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"msg": "User already register"})



@router.get("", status_code=status.HTTP_200_OK)
async def filter_users_list(
    q: str = Query(..., max_length=128),
    age: int = Query(None, ge=0),
    gender: GenderEnum = GenderEnum.female,
    page: int = 1,
    limit: PageLimitEnum = PageLimitEnum.small
):
    # TODO implement
    return {q, age, gender, page, limit}


@router.get("/me")
async def get_user_info(auth_user=Depends(get_user_with_claims), users_repo: UserRepository = Depends(get_repository(UserRepository))):
    user = await users_repo.get_user_by_id(auth_user.custom_claims.get('ref'))
    if user is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user, exclude_defaults=True, by_alias=False))
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/professionals/patients")
async def get_patients_by_professional(
        auth_professional_user=Depends(get_professional_user),
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
        page: int = Query(..., ge=1),
        limit: PageLimitEnum = PageLimitEnum.small
    ):
    user_id = auth_professional_user.custom_claims.get('ref')
    patiens = await users_repo.get_patients(professional_id=user_id, page_num=page, page_size=limit)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            patiens, exclude_defaults=True, by_alias=False)
    )

@router.put("/{user_id}/device-token")
async def set_device_token(
    user_id: str,
    token: str = Body(...),
    auth_user=Depends(get_user_with_claims),
    users_repo: UserRepository = Depends(get_repository(UserRepository))
):
    if auth_user.custom_claims.get('ref') != user_id:
        raise HTTPException(status_code=401, detail="User has not authorized")

    response = await users_repo.set_user_device_token(user_id=user_id, token=token)
    # TODO add validator or errro handlers
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response)
        
