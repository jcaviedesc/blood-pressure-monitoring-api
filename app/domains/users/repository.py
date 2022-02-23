from ...db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import UserCreate


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: UserCreate) -> UserCreate:
        user_body = jsonable_encoder(user, exclude_defaults=True)
        new_user = await self.db.users.insert_one(user_body)
        user_result = await self.db.users.find_one({"_id": new_user.inserted_id})
        return UserCreate(**user_result)
