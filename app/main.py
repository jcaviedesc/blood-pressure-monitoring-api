import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from .domains.api import router as api_router

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.clientdb = AsyncIOMotorClient(os.getenv("DATABASE_CONNECTION_URI"))
    app.database = app.clientdb[os.getenv("DATABASE_NAME")]
    print("start blood pressure Api Ok..")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.clientdb.close()
    
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)