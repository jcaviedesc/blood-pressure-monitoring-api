from typing import Optional
from loguru import logger
from fastapi.encoders import jsonable_encoder
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from .models import ClinicalMonitoringRequestsCreateModel


class ClinicalMonitoringRequestsRepository(BaseRepository):
    """"
    All database actions associated with the RequestsClinalHistory entity
    """
    async def create(self, requestsClinicalMonitoring: ClinicalMonitoringRequestsCreateModel, *, exclude_fields: Optional[list[str]] = None) -> ClinicalMonitoringRequestsCreateModel | None:
        """
        return a ClinicalMonitoringRequestsCreateModel if insert into database is succesfull otherwise None.
        """
        request_access = jsonable_encoder(
            requestsClinicalMonitoring, by_alias=True, exclude_none=True)
        try:
            new_request = await self.get_entity('ClinicalMonitoringRequests').insert_one(request_access)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields(exclude_fields)
        request_result = await self.get_entity('ClinicalMonitoringRequests').find_one({"_id": new_request.inserted_id}, projection)
        return ClinicalMonitoringRequestsCreateModel(**request_result)

    async def update(
        self,
        request_id: str,
        *,
        payload,
        exclude_fields: Optional[list[str]] = None
    ) -> ClinicalMonitoringRequestsCreateModel | None:
        """
        Update one request by _id and return true if the request was updated successful otherwise return false.
        """
        update_body = jsonable_encoder(
            payload, by_alias=True, exclude_none=True)
        try:
            updated_request = await self.get_entity('ClinicalMonitoringRequests').update_one(
                {"_id": request_id},
                {
                    '$set': update_body,
                    '$currentDate': {'utd_at': True}
                })
            if updated_request.modified_count:
                projection = make_excluded_fields(exclude_fields)
                request_result = await self.get_entity('ClinicalMonitoringRequests').find_one(
                    {"_id": request_id}, projection)
                return ClinicalMonitoringRequestsCreateModel(**request_result)
        except Exception as err:
            logger.error(err)
            # TODO agregar errorhandler
            return None
