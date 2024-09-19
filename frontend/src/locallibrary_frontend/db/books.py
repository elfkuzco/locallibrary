import datetime
from dataclasses import dataclass

from sqlalchemy import UnaryExpression, asc, desc, func, select, true
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.categories import get_or_create_category
from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import Book, BookInstance, Category, User
from locallibrary_frontend.db.publisher import get_or_create_publisher
from locallibrary_frontend.enums import BookSortColumnEnum, SortDirectionEnum
from locallibrary_frontend.settings import Settings


def get_book_or_one(session: OrmSession, isbn: str) -> Book | None:
    """Get a book from the database if it exists."""
    return session.scalars(select(Book).where(Book.isbn == isbn)).one_or_none()


def get_book(session: OrmSession, isbn: str) -> Book:
    """Get a book from the database."""
    book = get_book_or_one(session, isbn)
    if book is None:
        raise RecordDoesNotExistError(f"Book with isbn {isbn!r} does not exist.")
    return book


@dataclass
class BookListResult:
    """Result of query to list books from the database."""

    nb_books: int
    books: list[Book]


def filter_book(
    book: Book,
    *,
    publishers: list[str] | None = None,
    category: str | None = None,
    is_available: bool | None = None,
) -> bool:
    """Checks if a book has the same attribute as the provided attributes.

    Base logic for filtering a book from a database.
    Used by test code to validate return values from list_books.
    """
    # If a value was set (i.e not None), we ensure the attribute matches
    # the value.
    if is_available is not None:
        matching_availability = [
            instance
            for instance in book.instances
            if instance.is_available == is_available
        ]
        if not matching_availability:
            return False
    if category is not None:
        matching_category = [
            db_category
            for db_category in book.categories
            if db_category.name == category
        ]
        if not matching_category:
            return False
    if publishers is not None and book.publisher_name not in publishers:
        return False

    return True


def list_books(
    session: OrmSession,
    *,
    publishers: list[str] | None = None,
    category: str | None = None,
    is_available: bool | None = None,
    page_num: int = 1,
    page_size: int = Settings.MAX_PAGE_SIZE,
    sort_column: BookSortColumnEnum = BookSortColumnEnum.created_at,
    sort_direction: SortDirectionEnum = SortDirectionEnum.asc,
) -> BookListResult:
    """List books in the database."""

    if sort_direction == SortDirectionEnum.asc:
        direction = asc
    else:
        direction = desc

    # By default, we want to sort books on created_at. However, if a client
    # provides a sort_column, we give their sort_column a higher priority
    order_by: tuple[UnaryExpression[str], ...]
    if sort_column != BookSortColumnEnum.created_at:
        order_by = (
            direction(sort_column.name),
            asc(BookSortColumnEnum.created_at.name),
        )
    else:
        order_by = (direction(sort_column.name),)

    # If a client provides an argument i.e it is not None, we compare the corresponding
    # model field against the argument, otherwise, we compare the argument to
    # its default in the database which translates to a SQL true i.e we don't
    # filter based on this argument.
    query = (
        select(func.count().over().label("total_records"), Book)
        .join(BookInstance)
        .where(
            (BookInstance.is_available == is_available) | (is_available is None),
            (Book.publisher_name.in_(publishers if publishers else []))
            | (publishers is None),
            (Book.categories.any(name=category)) | (category is None),
        )
        .distinct(Book.isbn)
        .order_by(Book.isbn, *order_by)
        .offset((page_num - 1) * page_size)
        .limit(page_size)
    )
    result = BookListResult(nb_books=0, books=[])

    for total_records, book in session.execute(query).all():
        # Because the SQL window function returns the total_records
        # for every row, assign that value to the nb_books
        result.nb_books = total_records
        result.books.append(book)

    return result


def create_book(
    session: OrmSession,
    *,
    isbn: str,
    title: str,
    publisher_name: str,
    categories: list[str],
    summary: str | None = None,
    is_available: bool = True,
) -> Book:
    """Add a book to the database."""
    book = Book(isbn=isbn, title=title, summary=summary)

    book.publisher = get_or_create_publisher(session, publisher_name)
    book.instances.append(BookInstance(is_available=is_available))
    session.add(book)

    book_categories: list[Category] = []

    for category_name in set(categories):
        category = get_or_create_category(session, category_name)
        book_categories.append(category)

    book.categories = book_categories

    session.add(book)
    return book


def get_available_book_instances(session: OrmSession, isbn: str) -> list[BookInstance]:
    """Get available copies of the book."""
    return list(
        session.scalars(
            select(BookInstance).where(
                BookInstance.is_available == true(), BookInstance.book_isbn == isbn
            )
        ).all()
    )


def borrow_book(
    session: OrmSession,
    borrower: User,
    book_instance: BookInstance,
    due_date: datetime.datetime,
) -> BookInstance:
    """Mark a copy of a book as borrowed by user."""

    book_instance.is_available = False
    book_instance.due_date = due_date
    book_instance.borrower = borrower

    session.add(book_instance)
    session.flush()

    return book_instance
