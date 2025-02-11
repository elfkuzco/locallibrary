from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from locallibrary_frontend.db import upgrade_db_schema
from locallibrary_frontend.routes import auth, book, user
from locallibrary_frontend.routes.middleware import (
    AuthorizationHeaderFromCookieMiddleware,
)
from locallibrary_frontend.settings import Settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    upgrade_db_schema()
    yield


def create_app(*, debug: bool = True):
    app = FastAPI(debug=debug, docs_url="/", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=Settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        AuthorizationHeaderFromCookieMiddleware,
        cookie_name=Settings.ACCESS_TOKEN_NAME,
    )

    app.include_router(router=book.router)
    app.include_router(router=auth.router)
    app.include_router(router=user.router)

    return app


app = create_app()
