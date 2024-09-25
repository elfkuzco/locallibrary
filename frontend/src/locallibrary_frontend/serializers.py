from locallibrary_frontend import schemas
from locallibrary_frontend.db import models


def serialize_user(user: models.User) -> schemas.User:
    """Serialize a database user to a pydantic model."""
    return schemas.User(
        first_name=user.first_name, last_name=user.last_name, email=user.email
    )


def serialize_book(book: models.Book) -> schemas.Book:
    return schemas.Book(
        isbn=book.isbn,
        title=book.title,
        summary=book.summary,
        created_at=book.created_at,
        publisher_name=book.publisher_name,
        categories=[category.name for category in book.categories],
        copies=[
            schemas.BookInstance(
                is_available=instance.is_available,
                borrower_id=instance.borrower_id,
                due_date=instance.due_date,
            )
            for instance in book.instances
        ],
    )


def serialize_borrowed_book(book_instance: models.BookInstance) -> schemas.BorrowedBook:
    return schemas.BorrowedBook(
        is_available=book_instance.is_available,
        borrower_id=book_instance.borrower_id,
        due_date=book_instance.due_date,
        isbn=book_instance.book.isbn,
        title=book_instance.book.title,
        publisher_name=book_instance.book.publisher_name,
        summary=book_instance.book.summary,
        created_at=book_instance.book.created_at,
        categories=[category.name for category in book_instance.book.categories],
    )
