from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import User
from locallibrary_frontend.settings import Settings


def get_user_or_one(session: OrmSession, email: str) -> User | None:
    """Get a user from the database if it exists."""
    return session.scalars(select(User).where(User.email == email)).one_or_none()


def get_user(session: OrmSession, email: str) -> User:
    """Get a user from the database."""
    user = get_user_or_one(session, email)
    if user is None:
        raise RecordDoesNotExistError(
            f"User with email address {email!r} does not exist."
        )
    return user


def create_user(
    session: OrmSession,
    *,
    email: str,
    user_id: str,
    first_name: str | None,
    last_name: str | None,
) -> User:
    """Add a user to the database."""
    session.execute(
        insert(User)
        .values(email=email, first_name=first_name, last_name=last_name, id=user_id)
        .on_conflict_do_update(
            index_elements=["id"],
            set_={"first_name": first_name, "last_name": last_name},
        )
    )
    return get_user(session, email)


@dataclass
class UserListResult:
    """Result of query to list books from the database."""

    nb_users: int
    users: list[User]


def list_users(
    session: OrmSession,
    *,
    page_num: int = 1,
    page_size: int = Settings.MAX_PAGE_SIZE,
) -> UserListResult:
    """List users in the database."""

    query = (
        select(func.count().over().label("total_records"), User)
        .order_by(User.created_at.desc())
        .offset((page_num - 1) * page_size)
        .limit(page_size)
    )
    result = UserListResult(nb_users=0, users=[])

    for total_records, user in session.execute(query).all():
        # Because the SQL window function returns the total_records
        # for every row, assign that value to the nb_users
        result.nb_users = total_records
        result.users.append(user)

    return result
