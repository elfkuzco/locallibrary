from typing import Annotated

from fastapi import APIRouter, Depends

from locallibrary_frontend import schemas, serializers
from locallibrary_frontend.db import models
from locallibrary_frontend.routes.dependencies import (
    get_authenticated_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile")
async def user_profile(
    user: Annotated[models.User, Depends(get_authenticated_user)]
) -> schemas.User:
    return serializers.serialize_user(user)
