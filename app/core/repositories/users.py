from typing import Optional, Literal
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from fastapi.encoders import jsonable_encoder
from ..models.users import PatientUserCreate, ProfessionalUserCreate, UserCreatedModel, UserUpdateLinkedProfessionals


class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, user: PatientUserCreate | ProfessionalUserCreate, exclude_fields: Optional[list[str]] = None) -> UserCreatedModel | None:
        """
        return a UserCreatedModel if insert into database is succesfull otherwise None.
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
        user_result = await self.get_entity('Users').find_one({"_id": id}, projection)
        return UserCreatedModel(**user_result) if user_result is not None else None

    async def get_user_by_document_id(self, document: str, exclude_fields: Optional[list[str]] = None):
        projection = make_excluded_fields(exclude_fields)
        user_result = await self.get_entity('Users').find_one({"doc_id": document}, projection)
        return UserCreatedModel(**user_result) if user_result is not None else None

    async def get_patients(self, *, professional_id: str, page_size: int, page_num: int):
        """returns a set of Users documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)
        query = {
            'linked_professionals': professional_id,
        }
        projection = make_excluded_fields()
        cursor = self.get_entity('Users').find(
            query, projection).skip(skips).limit(page_size)

        patients = []
        for document in await cursor.to_list(length=page_size):
            patients.append(UserCreatedModel(**document))

        return patients

    async def set_user_device_token(self, *, user_id: str, token: str) -> Literal['success', 'failed']:
        update_token = await self.get_entity('Devices').update_one(
            {"user_id": user_id},
            {
                '$set': {
                    "token": token
                },
                '$currentDate': {'utd_at': True}
            },
            upsert=True)
        if update_token.modified_count > 0 or update_token.upserted_id is not None:
            return "success"
        else:
            return "failed"

    async def update_linked_specialists(self, *, patient_id: str, specialist_id: str) -> UserUpdateLinkedProfessionals | None:
        try:
            updated_user = await self.get_entity('Users').update_one(
                {"_id": patient_id},
                {
                    "$push": {"linked_professionals": specialist_id},
                    "$currentDate": {"utd_at": True}
                })
            # TODO que pasa si se acutaliza pero falla al obtener al data del usuario?
            if updated_user.modified_count > 0:
                projection = make_excluded_fields()
                user_result = await self.get_entity('Users').find_one(
                    {"_id": patient_id},
                    {**projection, "linked_professionals": 1}
                )
                return UserUpdateLinkedProfessionals(**user_result)
            else:
                return None
        except:
            return None
