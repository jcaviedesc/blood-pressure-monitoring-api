from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from loguru import logger
from starlette import status
from fastapi.encoders import jsonable_encoder
from firebase_admin import auth
from ...dependencies.database import get_repository
from ...dependencies.authorization import get_user, get_active_user
from ...core.responseModels import NotFoundResponse
from ...core.enums import PageLimitEnum
from .repository import UserRepository
from .schemas import InitialUserSchema, UserSchema
from .models import GenderEnum, IntitalUserCreate, UserCreate


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=IntitalUserCreate, status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: InitialUserSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> JSONResponse:
    initial_user = IntitalUserCreate(**new_user.dict())
    user_created = await users_repo.create_user(user=initial_user)

    if user_created:
        try:
            user = auth.create_user(
                phone_number=new_user.phone,
                display_name=new_user.full_name,
                disabled=True)
            logger.info("user {} created in fba".format(user.uid))
        except Exception as fba_err:
            logger.error(fba_err)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user_created, exclude_defaults=True, by_alias=False))
    else:
        user_already = f'User with phone {new_user.phone} already register'
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"msg": user_already})


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
async def complete_create_user(
    user_id: str,
    user: UserSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_token=Depends(get_user)
):
    user_complete = UserCreate(**user.dict())
    user_complete.calculate_vars()
    user_complete.set_is_complete()
    try:
        user_updated = await users_repo.update_user(user=user_complete, user_id=user_id)
    except Exception as db_error:
        # TODO mejorar
        logger.error(db_error)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Sorry! we have some problems to process your request"})

    if user_updated:
        try:
            params = {"display_name": user_updated.full_name, "disabled": False}
            if (profile_url := user_updated.avatar) is not None:
                params["photo_url"] = profile_url
            auth.update_user(user_token['uid'], **params)
        except ValueError as err:
            # Panic send report for reprosed updated user
            logger.info("There was a error updating user with ID {} in the auth provider".format(
                user_updated.id))
            logger.error(err)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user_updated, exclude_defaults=True, by_alias=False))
    else:
        # TODO add i18-n
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"msg": "User already register"})


@router.get("/{phone}", status_code=status.HTTP_200_OK)
async def find_user(
    phone: str,
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_token=Depends(get_active_user),
    action: str | None = None
) -> JSONResponse:
    # TODO handle access_authorization by permissions only the same user can access
    # and user_type = 2 with authorization.
    user = await users_repo.find_by_phone_number(phone_number=phone)
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user, exclude_defaults=True, by_alias=False))
    else:
        not_found = NotFoundResponse(
            'user with phone_number {} not found'.format(phone))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=not_found.toJson())


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
