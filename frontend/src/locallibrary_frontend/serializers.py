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
