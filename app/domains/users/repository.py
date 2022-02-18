from ...db.repositoryBase import BaseRepository
from fastapi.encoders import jsonable_encoder
from .models import UserCreate, UserInDB


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: UserCreate) -> UserInDB:
        user_body = jsonable_encoder(user)
        new_user = await self.db.users.insert_one(user_body)
        user_result = await self.db.users.find_one({"_id": new_user.inserted_id})
        return UserInDB(**user_result)
