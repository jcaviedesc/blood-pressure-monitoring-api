from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED
from app.dependencies.database import get_repository
from .repository import UserRepository
from .schemas import UserSchema
from .models import UserCreate, UserPublic


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserPublic, status_code=HTTP_201_CREATED)
async def create_user(
    new_user: UserSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository))
) -> UserPublic:
    user_encoder = UserCreate(**new_user.dict())
    created_user = await users_repo.create_user(user=user_encoder)
    return created_user
