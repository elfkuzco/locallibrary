import pytest
from faker import Faker
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.books import (
    create_book,
    filter_book,
    get_book,
    list_books,
    remove_book,
)
from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import Book


def test_book_does_not_exist(dbsession: OrmSession):
    """Check that a book does not exist in the database."""
    with pytest.raises(RecordDoesNotExistError):
        get_book(dbsession, isbn="doesnotexist")


def test_create_book(dbsession: OrmSession, data_gen: Faker):
    """Check that we can create a book in the database."""
    isbn = data_gen.isbn13()
    title = "abc"
    publisher_name = "appress"
    categories = ["fiction", "non-fiction"]
    summary = data_gen.paragraph()
    book = create_book(
        dbsession,
        isbn=isbn,
        title=title,
        publisher_name=publisher_name,
        categories=categories,
        summary=summary,
    )
    assert book.isbn == isbn
    assert book.title == title
    assert book.publisher is not None
    assert book.publisher.name == publisher_name
    assert book.summary == summary
    assert len(book.categories) == len(categories)
    assert len(book.instances) > 0
    for category in book.categories:
        assert category.name in categories


@pytest.mark.num_books(1)
def test_get_book(dbsession: OrmSession, books: list[Book]):
    existing_book = books[0]
    book = get_book(dbsession, existing_book.isbn)
    assert book == existing_book


@pytest.mark.parametrize(
    ["publishers", "category", "is_available", "expected"],
    [
        (None, None, None, True),
        (["n/a"], None, None, False),
        (None, "n/a", None, False),
        (None, None, True, True),
        (["Manning", "Appress"], "Technology", True, True),
    ],
)
def test_basic_filter(
    dbsession: OrmSession,
    data_gen: Faker,
    *,
    publishers: list[str] | None,
    category: str | None,
    is_available: bool | None,
    expected: bool,
):
    book = create_book(
        dbsession,
        isbn=data_gen.isbn13(),
        title=data_gen.text(max_nb_chars=30),
        publisher_name="Manning",
        categories=["Technology", "Science"],
        summary=data_gen.paragraph(),
    )
    assert (
        filter_book(
            book, publishers=publishers, category=category, is_available=is_available
        )
        == expected
    )


@pytest.mark.num_books(100)
@pytest.mark.parametrize(
    ["publishers", "category", "is_available"],
    [
        (None, None, None),  # list all books
        (None, None, True),  # list only available books
        (["Manning", "Appress"], None, None),  # list all books from the publishers
        (
            ["Manning", "Appress"],
            None,
            True,
        ),  # list available books from the publishers
        (None, "Fiction", None),  # list all fiction books
        (None, "Fiction", True),  # list fiction books that are available
        (["Manning", "Appress"], "Fiction", True),  # list books that match all criteria
    ],
)
def test_list_books(
    dbsession: OrmSession,
    books: list[Book],
    publishers: list[str] | None,
    category: str | None,
    is_available: bool | None,
):
    filtered_books = [
        book
        for book in books
        if filter_book(
            book, publishers=publishers, category=category, is_available=is_available
        )
    ]
    result = list_books(
        dbsession,
        publishers=publishers,
        category=category,
        page_size=len(books),
        is_available=is_available,
    )
    assert len(filtered_books) == result.nb_books


def test_remove_non_existing_book(dbsession: OrmSession):
    with pytest.raises(RecordDoesNotExistError):
        remove_book(dbsession, "doesnotexist")


@pytest.mark.num_books(1)
def test_remove_existing_book(dbsession: OrmSession, books: list[Book]):
    book = books[0]
    assert remove_book(dbsession, book.isbn) is None
