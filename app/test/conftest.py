from typing import Any
from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.domains.api import router as api_router
from app.dependencies.database import get_database


load_dotenv()


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = start_application()
    _app.clientdb = AsyncIOMotorClient(os.getenv("DATABASE_CONNECTION_URI"))
    _app.database = _app.clientdb[os.getenv("DATABASE_NAME")]
    yield _app
    _app.clientdb.close()


@pytest.fixture(scope="function")
def test_app(app: FastAPI) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    def _get_test_db():
        try:
            #TODO change to database by unit-testing?
            yield app.clientdb["TrackingBPdb"]
        finally:
            pass

    app.dependency_overrides[get_database] = _get_test_db

    with TestClient(app) as client:
        yield client


# @pytest.fixture(scope="module")
# def test_app():
#     client = TestClient(app)
#     yield client  # testing happens here
