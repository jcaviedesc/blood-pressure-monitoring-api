from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED
from fastapi.encoders import jsonable_encoder
from firebase_admin import auth
from ...dependencies.database import get_repository
from ...dependencies.authorization import get_user
from .repository import UserRepository
from .schemas import UserSchema
from .models import UserCreate, UserPublic


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserCreate, status_code=HTTP_201_CREATED)
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
