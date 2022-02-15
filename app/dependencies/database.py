from typing import Callable, Type
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import Depends
from starlette.requests import Request
from app.db.repositoryBase import BaseRepository

def get_database(request: Request) -> AsyncIOMotorDatabase:  
    return request.app.clientdb["TrackingBPdb"]  


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> Type[BaseRepository]:  
        return repo_type(db)  
    return get_repo