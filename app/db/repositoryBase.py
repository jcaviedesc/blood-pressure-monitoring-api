from typing import Literal
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

ENTITY = Literal['SelfcareTips', 'Users', 'BloodPressureMeasurements',
                 'Devices', 'Medicines', 'ClinicalMonitoringRequests']


class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def get_entity(self, entity_name: ENTITY) -> AsyncIOMotorCollection:
        # TODO add validation to access if exist ENTITY
        return self._db[entity_name]
