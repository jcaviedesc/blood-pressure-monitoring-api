from motor.motor_asyncio import AsyncIOMotorDatabase

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
