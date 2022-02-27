from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from fastapi.encoders import jsonable_encoder
from firebase_admin import auth
from ...dependencies.database import get_repository
from ...dependencies.authorization import get_user, get_active_user
from ...core.responseModels import NotFoundResponse
from ...core.enums import PageLimitEnum
from .repository import UserRepository
from .schemas import UserSchema
from .models import UserCreate, UserPublic, GenderEnum


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserCreate, status_code=HTTP_201_CREATED)
async def create_user(
    new_user: UserSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_token=Depends(get_user)
) -> UserPublic:
    user_encoder = UserCreate(**new_user.dict())
    user_encoder.calculate_vars()
    created_user = await users_repo.create_user(user=user_encoder)

    # TODO handle error
    auth.update_user(
        user_token['uid'],
        display_name=new_user.full_name,
        photo_url=new_user.profile_url)

    return JSONResponse(status_code=HTTP_201_CREATED, content=jsonable_encoder(created_user, exclude_defaults=True, by_alias=False))


@router.get("/{phone}", status_code=HTTP_200_OK)
async def find_user(
    phone: str,
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_token=Depends(get_active_user)
) -> UserPublic:
    # TODO handle access_authorization by permissions only the same user can access
    # and user_type = 2 with authorization.
    user = await users_repo.find_by_phone_number(phone_number=phone)
    if user:
        return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(user, exclude_defaults=True, by_alias=False))
    else:
        not_found = NotFoundResponse(
            'user with phone_number {} not found'.format(phone))
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=not_found.toJson())


@router.get("", status_code=HTTP_200_OK)
async def filter_users_list(
    q: str = Query(..., max_length=128),
    age: int = Query(None, ge=0),
    gender: GenderEnum = None,
    page: int = 1,
    limit: PageLimitEnum = PageLimitEnum.small
):
    # TODO implement 
    return {q, age, gender, page, limit}
