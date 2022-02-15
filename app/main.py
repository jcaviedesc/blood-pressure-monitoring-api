import os
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.domains.api import router as api_router

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.clientdb = AsyncIOMotorClient(os.getenv("DATABASE_CONNECTION_URI"))
    app.database = app.clientdb[os.getenv("DATABASE_NAME")]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    
app.include_router(api_router)
