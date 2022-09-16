from typing import Optional, Literal
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from fastapi.encoders import jsonable_encoder
from ..models.devices import DeviceModel


class DevicesRepository(BaseRepository):
    """"
    All database actions associated with the Devices resource
    """
    async def get_device_by_user_id(self, user_id, *, exclude_fields: Optional[list[str]] = None) -> DeviceModel | None:
        """
        return a DeviceModel if there is device otherwise None.
        """
        projection = make_excluded_fields(exclude_fields)
        device = await self.get_entity('Devices').find_one({'user_id': user_id}, projection)
        return DeviceModel(**device) if device is not None else None
