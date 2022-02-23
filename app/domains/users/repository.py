from ...db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import UserCreate, UserPublic


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: UserCreate) -> UserCreate:
        user_body = jsonable_encoder(user, exclude_defaults=True)
        new_user = await self.db.users.insert_one(user_body)
        user_result = await self.db.users.find_one({"_id": new_user.inserted_id})
        return UserCreate(**user_result)

    async def find_by_phone_number(self, *, phone_number: str) -> UserPublic | None:
        user_result = await self.db.users.find_one({"phone_number": phone_number})
        return UserPublic(**user_result) if user_result is not None else None