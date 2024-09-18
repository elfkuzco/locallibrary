from contextlib import asynccontextmanager

from fastapi import FastAPI

from locallibrary_frontend.db import upgrade_db_schema
from locallibrary_frontend.routes import book, user


@asynccontextmanager
async def lifespan(_: FastAPI):
    upgrade_db_schema()
    yield


def create_app(*, debug: bool = True):
    app = FastAPI(debug=debug, docs_url="/", lifespan=lifespan)

    app.include_router(router=user.router)
    app.include_router(router=book.router)

    return app


app = create_app()
