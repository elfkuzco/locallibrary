import os
from typing import Any


def getenv(key: str, *, mandatory: bool = False, default: Any = None) -> Any:
    value = os.getenv(key, default=default)

    if mandatory and not value:
        raise OSError(f"Please set the {key} environment variable.")

    return value


class Settings:
    """Frontend API configuration"""

    DATABASE_URL: str = getenv("POSTGRES_URI", mandatory=True)
    DEBUG = bool(getenv("DEBUG", default=False))
    # maximum number of items to return from a request/query
    MAX_PAGE_SIZE = int(getenv("PAGE_SIZE", default=20))
    GRPC_SERVER_PORT = int(getenv("GRPC_SERVER_PORT", default=50051))
