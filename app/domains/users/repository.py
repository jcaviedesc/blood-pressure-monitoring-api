from typing import Optional
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from fastapi.encoders import jsonable_encoder
from .models import IntitalUserCreate, UserPublic, UserCreate, UserUpdate


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: IntitalUserCreate, exclude_fields: Optional[list[str]] = None) -> IntitalUserCreate | None:
        user_body = jsonable_encoder(user, by_alias=True)
        try:
            new_user = await self.db.users.insert_one(user_body)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields(exclude_fields)
        user_result = await self.db.users.find_one({"_id": new_user.inserted_id}, projection)
        return IntitalUserCreate(**user_result)

    async def update_user(self, *, user: UserCreate | UserUpdate, user_id: str, exclude_fields: Optional[list[str]] = None) -> UserPublic | None:
        user_body = jsonable_encoder(user, by_alias=True)
        updated_user = await self.db.users.update_one({'_id': user_id}, {'$set': user_body, '$currentDate': {'upAt': True}})
        if updated_user.modified_count > 0:
            projection = make_excluded_fields(exclude_fields)
            user_result = await self.db.users.find_one({"_id": user_id}, projection)
            return UserPublic(**user_result)
        return None

    async def find_by_phone_number(self, *, phone_number: str) -> UserPublic | None:
        user_result = await self.db.users.find_one({"phone_number": phone_number})
        return UserPublic(**user_result) if user_result is not None else None
