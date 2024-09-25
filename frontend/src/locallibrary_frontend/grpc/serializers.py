# pyright: strict, reportMissingTypeStubs=false,reportUnknownMemberType=false
from google.protobuf.timestamp_pb2 import Timestamp
from locallibrary_frontend_grpc import frontend_pb2 as pb

from locallibrary_frontend.db.models import Book, BookInstance, User
from locallibrary_frontend.schemas import Paginator


def serialize_book(
    book: Book, *, only_unavailable_copies: bool = False
) -> pb.BookDetail:
    """Convert a db book to the gRPC model.

    If only_unavailable_copies, only borrowed copies are added to
    the copies attribute, otherwise, all copies of the book.
    """
    if only_unavailable_copies:
        book_instances = book.borrowed_instances
    else:
        book_instances = book.instances
    return pb.BookDetail(
        isbn=book.isbn,
        title=book.title,
        publisher_name=book.publisher_name,
        created_at=Timestamp().FromDatetime(book.created_at),
        summary=book.summary,
        categories=[category.name for category in book.categories],
        copies=[
            pb.BookInstance(
                id=str(instance.id),
                borrower_id=instance.borrower_id,
                due_date=(
                    Timestamp().FromDatetime(instance.due_date)
                    if instance.due_date
                    else None
                ),
                is_available=instance.is_available,
            )
            for instance in book_instances
        ],
    )


def serialize_borrowed_book(book_instance: BookInstance) -> pb.BorrowedBook:
    """Convert a db book copy to the gRPC model."""
    return pb.BorrowedBook(
        is_available=book_instance.is_available,
        borrower_id=book_instance.borrower_id,
        due_date=(
            Timestamp().FromDatetime(book_instance.due_date)
            if book_instance.due_date
            else None
        ),
        isbn=book_instance.book.isbn,
        title=book_instance.book.title,
        publisher_name=book_instance.book.publisher_name,
        summary=book_instance.book.summary,
        created_at=Timestamp().FromDatetime(book_instance.book.created_at),
        categories=[category.name for category in book_instance.book.categories],
    )


def serialize_user(user: User) -> pb.UserDetail:
    """Convert a db user to the gRPC model including borrowed books by user."""
    return pb.UserDetail(
        email=user.email,
        last_name=user.last_name,
        first_name=user.first_name,
        created_at=Timestamp().FromDatetime(user.created_at),
        borrowed_books=[
            serialize_borrowed_book(book_instance)
            for book_instance in user.borrowed_books
        ],
    )


def serialize_user_without_books(user: User) -> pb.User:
    """Convert a db user to the gRPC model without the list of borrowed books."""
    return pb.User(
        email=user.email,
        last_name=user.last_name,
        first_name=user.first_name,
        created_at=Timestamp().FromDatetime(user.created_at),
    )


def serialize_paginator(paginator: Paginator) -> pb.Paginator:
    """Convert a pydantic paginator to the gRPC model."""
    return pb.Paginator(
        total_records=paginator.total_records,
        page_size=paginator.page_size,
        current_page=paginator.current_page,
        first_page=paginator.first_page,
        last_page=paginator.last_page,
    )
