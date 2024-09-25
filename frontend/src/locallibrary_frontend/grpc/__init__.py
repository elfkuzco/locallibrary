from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db import Session


@contextmanager
def grpc_dbsession() -> Generator[OrmSession, Any, None]:
    with Session.begin() as session:
        yield session
