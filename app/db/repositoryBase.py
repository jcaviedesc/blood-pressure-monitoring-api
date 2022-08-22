from enum import Enum
from typing import Literal
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

ENTITY = Literal['SelfcareTips', 'Users', 'BloodPressureMeasurements']
class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def get_entity(self, entity_name: ENTITY) -> AsyncIOMotorCollection:
        return self._db[entity_name]
