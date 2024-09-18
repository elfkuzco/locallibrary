from collections.abc import Generator
from typing import Any

import pytest
from faker import Faker
from faker.providers import DynamicProvider
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db import Session
from locallibrary_frontend.db.books import create_book
from locallibrary_frontend.db.models import Base, Book, User


@pytest.fixture(autouse=True)
def dbsession() -> Generator[OrmSession, None, None]:
    """Set up a database session for tests."""
    with Session.begin() as session:
        # Ensure we are starting with an empty database
        engine = session.get_bind()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield session
        session.rollback()


@pytest.fixture
def data_gen(faker: Faker) -> Faker:
    """Adds additional providers to faker.

    Registers book_publisher as a provider.
    data_gen.book_publisher() returns a book publisher.
    All other providers from Faker can be used accordingly.
    """
    book_publisher_provider = DynamicProvider(
        provider_name="book_publisher",
        elements=[
            "Appress",
            "Manning",
            "O'Reilly",
            "The Pragmatic Programmers",
        ],
    )
    faker.add_provider(book_publisher_provider)
    faker.seed_instance(123)
    return faker


@pytest.fixture
def users(
    dbsession: OrmSession,
    data_gen: Faker,
    request: Any,
) -> list[User]:
    """Adds users to the database using the num_users mark."""
    mark = request.node.get_closest_marker("num_users")
    if mark and len(mark.args) > 0:
        num_users = int(mark.args[0])
    else:
        num_users = 10

    users = [
        User(
            first_name=data_gen.first_name(),
            last_name=data_gen.last_name(),
            email=data_gen.ascii_email(),
        )
        for _ in range(num_users)
    ]
    dbsession.add_all(users)
    dbsession.flush()

    return users


@pytest.fixture
def books(
    dbsession: OrmSession,
    data_gen: Faker,
    request: Any,
) -> list[Book]:
    """Adds books to the database using the num_books mark."""
    mark = request.node.get_closest_marker("num_books")
    if mark and len(mark.args) > 0:
        num_books = int(mark.args[0])
    else:
        num_books = 10

    books = [
        create_book(
            dbsession,
            isbn=data_gen.isbn13(),
            summary=data_gen.paragraph(),
            title=data_gen.text(max_nb_chars=30),
            publisher_name=data_gen.book_publisher(),
            categories=data_gen.words(
                nb=3,
                ext_word_list=[
                    "Fiction",
                    "Non-Fiction",
                    "Thriller",
                    "Romance",
                    "History",
                ],
                unique=True,
            ),
            is_available=data_gen.pybool(),
        )
        for _ in range(num_books)
    ]
    return books
