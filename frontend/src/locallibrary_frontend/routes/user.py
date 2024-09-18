from fastapi import APIRouter
from fastapi import status as status_codes
from sqlalchemy.exc import IntegrityError

from locallibrary_frontend import schemas
from locallibrary_frontend.db.user import create_user as db_create_user
from locallibrary_frontend.routes.dependencies import DbSession
from locallibrary_frontend.routes.http_errors import RequestConflictError, ServerError
from locallibrary_frontend.serializers import serialize_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/create",
    status_code=status_codes.HTTP_200_OK,
    responses={
        status_codes.HTTP_200_OK: {"description": "User successfully created"},
        status_codes.HTTP_409_CONFLICT: {
            "description": "A user with the email already exists."
        },
    },
)
def create_user(session: DbSession, user_in: schemas.User):
    try:
        db_user = db_create_user(
            session,
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
        )
    except IntegrityError as exc:
        raise RequestConflictError("A user with the email already exists.") from exc
    except Exception as exc:
        raise ServerError() from exc
    return serialize_user(db_user)
