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
from ...dependencies.authorization import get_user, get_user_with_claims
from ...core.responseModels import NotFoundResponse
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
            user = PatientUserCreate(**new_user.dict())
            user.set_cardiovascular_risk()
        else:
            user = ProfessionalUserCreate(**new_user.dict())
    except ValidationError as err:
        raise RequestValidationError(errors=err.raw_errors)

    user.calculate_age().calculate_IMC()
    user_created = await users_repo.create_user(user=user)

    if user_created:
        try:
            params = {
                "display_name": f'{user_created.name} {user_created.last_name}'
            }
            if (profile_url := user_created.avatar) is not None:
                params["photo_url"] = profile_url

            uid_user = auth_user.get('uid')
            print(uid_user, auth_user)
            auth.update_user(uid_user, **params)
            auth.set_custom_user_claims(
                uid_user, {"isRegistered": True, "ref": str(user_created.id)})

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


# @router.get("/{phone}", status_code=status.HTTP_200_OK)
# async def find_user(
#     phone: str,
#     users_repo: UserRepository = Depends(get_repository(UserRepository)),
#     user_token=Depends(get_user),
#     action: str | None = None
# ) -> JSONResponse:
#     # TODO handle access_authorization by permissions only the same user can access
#     # and user_type = 2 with authorization.
#     user = await users_repo.find_by_phone_number(phone_number=phone)
#     if user:
#         return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user, exclude_defaults=True, by_alias=False))
#     else:
#         not_found = NotFoundResponse(
#             'user with phone_number {} not found'.format(phone))
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=not_found.toJson())


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
    if not user is None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user, exclude_defaults=True, by_alias=False))
    else:
        raise HTTPException(status_code=404, detail="User not found")
