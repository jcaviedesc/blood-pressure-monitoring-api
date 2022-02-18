from typing import Any
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="function")
def test_app() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    # def _get_test_db():
    #     try:
    #         # TODO change to database by unit-testing?
    #         yield app.clientdb["TrackingBPdb"]
    #     finally:
    #         pass

    # app.dependency_overrides[get_database] = _get_test_db

    with TestClient(app) as client:
        yield client
