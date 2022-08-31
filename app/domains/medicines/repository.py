from typing import Optional, Literal
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from .models import MedicineModelCreate

MAX_MEDICINES_PER_USER = 25
class MedicineRepository(BaseRepository):
    """"
    All database actions associated with the Medicines entity
    """
    async def add_medicine(self, *, medicine: MedicineModelCreate, exclude_fields: Optional[list[str]] = None) -> MedicineModelCreate | None:
        medicine_data = jsonable_encoder(
            medicine, by_alias=True, exclude_none=True)
        try:
            new_medicine = await self.get_entity('Medicines').insert_one(medicine_data)
        except:
            # TODO agregar error handler
            return None
        projection = make_excluded_fields(exclude_fields)
        user_result = await self.get_entity('Medicines').find_one({"_id": new_medicine.inserted_id}, projection)
        return MedicineModelCreate(**user_result)

    async def list_medicines(self,*, user_id: str):
        query = {
            'user_id': user_id,
        }
        projection = make_excluded_fields()
        cursor = self.get_entity('Medicines').find(query, projection).limit(MAX_MEDICINES_PER_USER)

        medicines =[]
        for document in await cursor.to_list(length=MAX_MEDICINES_PER_USER):
            medicines.append(MedicineModelCreate(**document))

        return medicines
