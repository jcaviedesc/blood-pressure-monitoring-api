from typing import Optional
from bson import ObjectId
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from fastapi.encoders import jsonable_encoder
from .models import PatientUserCreate, ProfessionalUserCreate, UserCreatedModel


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: PatientUserCreate | ProfessionalUserCreate, exclude_fields: Optional[list[str]] = None) -> UserCreatedModel | None:
        """returns a UserCreatedModel if insert into database is succesfull otherwise None.
        """
        user_body = jsonable_encoder(
            user, by_alias=True, exclude_none=True)
        try:
            new_user = await self.get_entity('Users').insert_one(user_body)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields(exclude_fields)
        user_result = await self.get_entity('Users').find_one({"_id": new_user.inserted_id}, projection)
        return UserCreatedModel(**user_result)

    async def get_user_by_id(self, id: str, exclude_fields: Optional[list[str]] = None):
        projection = make_excluded_fields(exclude_fields)
        user_result = await self.get_entity('Users').find_one({"_id": ObjectId(id)}, projection)
        return UserCreatedModel(**user_result) if not user_result is None else None

    async def get_patients(self, *, professional_id: str, page_size: int, page_num: int):
        """returns a set of Users documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)
        query = {
            "linked_professionals": professional_id,
        }
        projection = make_excluded_fields()
        cursor = await self.get_entity('Users').find(query, projection).skip(skips).limit(page_size)

        return [UserCreatedModel(**patient) for patient in cursor]

    # async def update_user(self, *, user: UserCreate | UserUpdate, user_id: str, exclude_fields: Optional[list[str]] = None) -> UserPublic | None:
    #     user_body = jsonable_encoder(user, by_alias=True)
    #     updated_user = await self.get_entity('Users').update_one({'_id': user_id}, {'$set': user_body, '$currentDate': {'upAt': True}})
    #     if updated_user.modified_count > 0:
    #         projection = make_excluded_fields(exclude_fields)
    #         user_result = await self.get_entity('Users').find_one({"_id": user_id}, projection)
    #         return UserPublic(**user_result)
    #     return None

    # async def find_by_phone_number(self, *, phone_number: str) -> UserPublic | None:
    #     user_result = await self.get_entity('Users').find_one({"phone_number": phone_number})
    #     return UserPublic(**user_result) if user_result is not None else None
