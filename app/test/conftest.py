from typing import Any
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies.authorization import get_user


@pytest.fixture(scope="function")
def test_app() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `_get_user_test` fixture to override
    the `get_user` dependency that is injected into routes.
    """
    def _get_user_test():
        try:
            print("using override get_user")
            yield {"uid": "tviO7LMCSeMSwrOPOkAaEmw8b6H2"}
        finally:
            pass

    app.dependency_overrides[get_user] = _get_user_test
    with TestClient(app) as client:
        yield client
