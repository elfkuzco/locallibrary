from typing import Annotated

import jwt
from fastapi import Depends, Request, Response
from sqlalchemy.orm import Session

from locallibrary_frontend.db import gen_dbsession
from locallibrary_frontend.db.models import User
from locallibrary_frontend.db.user import get_user_or_none
from locallibrary_frontend.routes import http_errors
from locallibrary_frontend.settings import Settings

DbSession = Annotated[Session, Depends(gen_dbsession)]


def get_user_id_from_access_token_or_none(
    request: Request,
    response: Response,
) -> str | None:
    # Add the "Vary: Authorization" header to the response.
    # This indicates to any caches that the response may vary
    # based on the value of the Authorization header in the
    # request
    response.headers.add_vary_header("Authorization")
    # Retrieve the value of the Authorization header from the
    # request. This will return the empty string "" if there
    # is no such header found.
    authorization_header = request.headers.get("Authorization", "")
    if authorization_header == "":
        return None

    # Otherwise, we expect the value of the Authorization header
    # to be in the format "Bearer <token>". we try to split this
    # into its constituent parts, and if the header isn't in the
    # expected format, we return a 401 Unauthorized response
    header_parts = authorization_header.split(" ")
    if len(header_parts) != 2 or header_parts[0] != "Bearer":  # noqa
        raise http_errors.InvalidAuthenticationTokenError()

    token = header_parts[1]

    # Parse the JWT and extract the claims. This will return an
    # error if the JWT contents don't match the signature (i.e.
    # the token has been tampered with) or the algorithm isn't
    # valid
    try:
        claims = jwt.decode(
            token,
            key=Settings.JWT_ECDSA_PUBLIC_KEY,
            algorithms=Settings.JWT_ALGORITHM,
            options={"require": ["exp", "sub", "iss", "aud", "iat", "exp"]},
            audience=[
                "locallibrary.admin.service",
                "locallibrary.frontend.service",
            ],
            issuer="locallibrary.frontend.service",
        )
    except jwt.ExpiredSignatureError as exc:
        raise http_errors.InvalidAuthenticationTokenError("Token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise http_errors.InvalidAuthenticationTokenError() from exc
    except Exception as exc:
        raise http_errors.ServerError() from exc
    return claims["sub"]


def get_user_from_access_token_or_none(
    user_id: Annotated[str | None, Depends(get_user_id_from_access_token_or_none)],
    db_session: DbSession,
):
    if user_id is None:
        return None
    return get_user_or_none(db_session, user_id)


def get_authenticated_user(
    user: Annotated[User | None, Depends(get_user_from_access_token_or_none)]
) -> User:
    if user is None:
        raise http_errors.UnauthorizedError()
    return user
