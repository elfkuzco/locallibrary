import base64
import os
from typing import Any

from humanfriendly import parse_timespan


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
    # oauth2 provider crdedentials
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID", mandatory=True)
    GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET", mandatory=True)
    # jwt settings
    JWT_ECDSA_PRIVATE_KEY = base64.standard_b64decode(
        getenv("JWT_ECDSA_PRIVATE_KEY", mandatory=True)
    ).decode()
    JWT_ECDSA_PUBLIC_KEY = base64.standard_b64decode(
        getenv("JWT_ECDSA_PUBLIC_KEY", mandatory=True)
    ).decode()
    JWT_EXPIRY_DURATION = parse_timespan(getenv("JWT_EXPIRY_DURATION", default="3h"))
    JWT_ALGORITHM = getenv("JWT_ALGORITHM", default="ES256")
