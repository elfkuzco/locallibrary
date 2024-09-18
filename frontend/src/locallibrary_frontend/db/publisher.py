from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import Publisher


def get_publisher_or_one(session: OrmSession, name: str) -> Publisher | None:
    """Get a publisher from the database if it exists."""
    return session.scalars(
        select(Publisher).where(Publisher.name == name)
    ).one_or_none()


def get_publisher(session: OrmSession, name: str) -> Publisher:
    """Get a publisher from the database."""
    publisher = get_publisher_or_one(session, name)
    if publisher is None:
        raise RecordDoesNotExistError(f"Publisher with name {name!r} does not exist.")
    return publisher


def get_or_create_publisher(session: OrmSession, name: str) -> Publisher:
    """Add a publisher to the database if it does not exist."""
    session.execute(
        insert(Publisher)
        .values(name=name)
        .on_conflict_do_nothing(index_elements=["name"])
    )
    return get_publisher(session, name)
