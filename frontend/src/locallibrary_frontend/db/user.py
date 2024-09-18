from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import User


def get_user_or_one(session: OrmSession, email: str) -> User | None:
    """Get a user from the database if it exists."""
    return session.scalars(select(User).where(User.email == email)).one_or_none()


def get_user(session: OrmSession, email: str) -> User:
    """Get a user from the database."""
    user = get_user_or_one(session, email)
    if user is None:
        raise RecordDoesNotExistError(
            f"User with provided email {email!r} does not exist."
        )
    return user


def create_user(
    session: OrmSession, *, email: str, first_name: str, last_name: str
) -> User:
    """Add a user to the database."""
    user = User(email=email, first_name=first_name, last_name=last_name)
    session.add(user)
    session.flush()
    return user
