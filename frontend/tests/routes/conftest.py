from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db import gen_dbsession
from locallibrary_frontend.web import app


@pytest.fixture
def client(dbsession: OrmSession) -> TestClient:
    def test_dbsession() -> Generator[OrmSession, None, None]:
        yield dbsession

    # Replace the  database session with the test dbsession
    app.dependency_overrides[gen_dbsession] = test_dbsession

    return TestClient(app=app)
