import os
import uvicorn
from loguru import logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from .domains.api import router as api_router
from .core.config import get_settings

settings = get_settings()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
settings.configure_logging()

app = FastAPI(**settings.fastapi_kwargs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.clientdb = AsyncIOMotorClient(settings.database_connection_uri)
    app.database = app.clientdb[settings.database_name]
    logger.info("Startup Blood Pressure API complete...")
    logger.info("Connection to {0} succesful", repr(settings.database_name))


@app.on_event("shutdown")
async def shutdown_db_client():
    app.clientdb.close()
    logger.info("Closing connection to database")

app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
