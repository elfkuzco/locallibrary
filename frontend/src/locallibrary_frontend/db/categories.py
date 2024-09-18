from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import Category


def get_category_or_one(session: OrmSession, name: str) -> Category | None:
    """Get a category from the database if it exists."""
    return session.scalars(select(Category).where(Category.name == name)).one_or_none()


def get_category(session: OrmSession, name: str) -> Category:
    """Get a publisher from the database."""
    category = get_category_or_one(session, name)
    if category is None:
        raise RecordDoesNotExistError(f"Category with name {name!r} does not exist.")
    return category


def get_or_create_category(session: OrmSession, name: str) -> Category:
    """Add a category to the database if it does not exist."""
    session.execute(
        insert(Category)
        .values(name=name)
        .on_conflict_do_nothing(index_elements=["name"])
    )
    return get_category(session, name)
