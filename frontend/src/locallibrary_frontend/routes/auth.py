import datetime
from typing import Annotated

import aiohttp
import jwt
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

from locallibrary_frontend import logger
from locallibrary_frontend.db.tokens import create_refresh_token
from locallibrary_frontend.db.user import create_user as db_create_user
from locallibrary_frontend.routes import http_errors
from locallibrary_frontend.routes.dependencies import (
    DbSession,
    get_user_id_from_access_token_or_none,
)
from locallibrary_frontend.schemas import AuthTokenStatus, RefreshToken, Token
from locallibrary_frontend.settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register/google/callback")
async def register_google_callback(
    code: str,
    request: Request,
    session: DbSession,
    next_path: Annotated[str | None, Query(alias="state")] = None,
):
    token_request_uri = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": Settings.GOOGLE_CLIENT_ID,
        "client_secret": Settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": request.url_for("register_google_callback"),
        "grant_type": "authorization_code",
    }

    async with aiohttp.ClientSession() as client:
        resp = await client.post(token_request_uri, data=data)
        try:
            resp.raise_for_status()
        except Exception as exc:
            logger.exception("error while requesting for token from google.")
            raise http_errors.ServerError() from exc
        oauth_data = await resp.json()

        # Use the access token to obtain the user's personal information
        access_token = oauth_data.get("access_token")
        resp = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        try:
            resp.raise_for_status()
        except Exception as exc:
            logger.exception("error while fetching user profile from google.")
            raise http_errors.ServerError() from exc
        user_data = await resp.json()

        # store the user in the database.
        try:
            db_user = db_create_user(
                session,
                email=user_data["email"],
                user_id=user_data["id"],
                first_name=user_data.get("given_name"),
                last_name=user_data.get("family_name"),
            )
        except IntegrityError as exc:
            raise http_errors.RequestConflictError(
                "A user with the email already exists."
            ) from exc
        except Exception as exc:
            logger.exception("error while creating user in datbase")
            raise http_errors.ServerError() from exc

        # save the refresh token for this user
        refresh_token = RefreshToken(
            token=oauth_data.get("refresh_token"), provider="google"
        )
        if refresh_token.token:
            create_refresh_token(
                session,
                user=db_user,
                token=refresh_token.token,
                provider=refresh_token.provider,
            )

        # Create a JWT claims payload containing the user ID as the subject,
        # with an issued time of now and validity window of the expiry duration.
        # We also set the issuer and audience to a unique identifier
        # for our application and other services.
        now = datetime.datetime.now(datetime.UTC)
        access_token = jwt.encode(
            payload={
                "sub": db_user.id,
                "iat": now,
                "nbf": now,
                "exp": now + datetime.timedelta(seconds=Settings.JWT_EXPIRY_DURATION),
                "iss": "locallibrary.frontend.service",
                "aud": [
                    "locallibrary.admin.service",
                    "locallibrary.frontend.service",
                ],
            },
            key=Settings.JWT_ECDSA_PRIVATE_KEY,
            algorithm=Settings.JWT_ALGORITHM,
        )

        if Settings.UI_BASE_URI and next_path:
            logger.info("saving tokens as cookies in browser.")
            # Set the token as a http cookie to be used in requests from
            # the allowed origins in web browsers.
            server_response = RedirectResponse(Settings.UI_BASE_URI + next_path)
            server_response.set_cookie(
                key=Settings.ACCESS_TOKEN_NAME,
                value=access_token,
                path="/",
                secure=True,
                httponly=True,
                samesite="none",
                expires=now + datetime.timedelta(seconds=Settings.JWT_EXPIRY_DURATION),
            )
            if refresh_token.token:
                # store the refresh token in the browser as a cookie.
                server_response.set_cookie(
                    key=Settings.REFRESH_TOKEN_NAME,
                    value=refresh_token.token,
                    path="/",
                    secure=True,
                    httponly=True,
                    samesite="none",
                    expires=None,
                )
            # redirect the next url as pointed by the frontend.
            # TODO: ensure next is a relative url
            return server_response
        else:
            return Token(access_token=access_token, token_type="Bearer")


@router.get("/verify")
async def verify_authentication_token(
    user_id: Annotated[str | None, Depends(get_user_id_from_access_token_or_none)]
):
    return AuthTokenStatus(is_valid=user_id is not None)
