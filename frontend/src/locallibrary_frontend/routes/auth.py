import datetime

import aiohttp
import jwt
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

from locallibrary_frontend.db.tokens import create_refresh_token
from locallibrary_frontend.db.user import create_user as db_create_user
from locallibrary_frontend.routes.dependencies import DbSession
from locallibrary_frontend.routes.http_errors import RequestConflictError, ServerError
from locallibrary_frontend.schemas import RefreshToken, Token
from locallibrary_frontend.settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register")
async def register(request: Request):
    redirect_uri = request.url_for("register_google_callback")
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={Settings.GOOGLE_CLIENT_ID}"
        f"&access_type=offline&redirect_uri={redirect_uri}"
        "&response_type=code&scope=openid email profile"
    )

    return RedirectResponse(url=google_auth_url)


@router.get("register/google/callback")
async def register_google_callback(
    code: str, request: Request, session: DbSession, server_response: Response
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
        resp.raise_for_status()
        oauth_data = await resp.json()

        # Use the access token to obtain the user's personal information
        access_token = oauth_data.get("access_token")
        resp = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        resp.raise_for_status()
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
            raise RequestConflictError("A user with the email already exists.") from exc
        except Exception as exc:
            raise ServerError() from exc

        # save the refresh token for this user
        refresh_token = RefreshToken(
            token=oauth_data["refresh_token"], provider="google"
        )
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

        # Set the token as a http cookie to be used in requests from
        # the allowed origins in web browsers.
        server_response.set_cookie(
            key="accessToken",
            value=access_token,
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
            expires=now + datetime.timedelta(seconds=Settings.JWT_EXPIRY_DURATION),
        )
        return Token(access_token=access_token, token_type="bearer")
