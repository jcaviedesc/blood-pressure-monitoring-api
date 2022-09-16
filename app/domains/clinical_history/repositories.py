from typing import Optional
from fastapi.encoders import jsonable_encoder
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from .models import ClinalHistoryRequestsCreateModel


class ClinalHistoryRequestsRepository(BaseRepository):
    """"
    All database actions associated with the RequestsClinalHistory entity
    """
    async def create(self, requestsClinicalHistory: ClinalHistoryRequestsCreateModel, *, exclude_fields: Optional[list[str]] = None) -> ClinalHistoryRequestsCreateModel | None:
        """
        return a ClinalHistoryRequestsCreateModel if insert into database is succesfull otherwise None.
        """
        request_access = jsonable_encoder(
            requestsClinicalHistory, by_alias=True, exclude_none=True)
        try:
            new_request = await self.get_entity('ClinalHistoryRequests').insert_one(request_access)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields(exclude_fields)
        request_result = await self.get_entity('ClinalHistoryRequests').find_one({"_id": new_request.inserted_id}, projection)
        return ClinalHistoryRequestsCreateModel(**request_result)
