from enum import Enum
from motor.motor_asyncio import AsyncIOMotorDatabase

class Entities(str, Enum):
    SELFCARE_TIPS = "SelfcareTips"
    USERS = "Users",
    BLOOD_PRESSURE_MEASUREMENTS = "BloodPressureMeasurements"

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def get_entity(self, entity_name: Entities):
        return self._db[entity_name]
