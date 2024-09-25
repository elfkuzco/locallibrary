# pyright: strict, reportMissingTypeStubs=false,reportUnknownMemberType=false
# ruff: noqa: N802,ARG002
from typing import cast

import grpc
from google.protobuf.empty_pb2 import Empty
from grpc_interceptor.exceptions import AlreadyExists, NotFound
from locallibrary_frontend_grpc import frontend_pb2 as pb
from locallibrary_frontend_grpc import frontend_pb2_grpc
from sqlalchemy.exc import IntegrityError

from locallibrary_frontend.db.books import create_book, list_books, remove_book
from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.user import get_user, list_users
from locallibrary_frontend.grpc import grpc_dbsession
from locallibrary_frontend.grpc.serializers import (
    serialize_book,
    serialize_paginator,
    serialize_user,
    serialize_user_without_books,
)
from locallibrary_frontend.schemas import calculate_pagination_metadata


class FrontendServicer(frontend_pb2_grpc.LocalLibraryFrontendServicer):
    """Provides methods that implement functionality for the frontend gRPC server."""

    def AddBook(
        self, request: pb.AddBookRequest, context: grpc.ServicerContext
    ) -> pb.BookDetail:
        """Add a book to the library."""
        with grpc_dbsession() as session:
            try:
                book = create_book(
                    session,
                    isbn=request.isbn,
                    title=request.title,
                    publisher_name=request.publisher_name,
                    categories=cast(list[str], request.categories),
                    summary=request.summary,
                )
            except IntegrityError as exc:
                raise AlreadyExists(
                    f"Book {request.isbn} already exists in the database."
                ) from exc
            return serialize_book(book)

    def RemoveBook(
        self, request: pb.RemoveBookRequest, context: grpc.ServicerContext
    ) -> Empty:
        """Remove a book from the library."""
        with grpc_dbsession() as session:
            try:
                remove_book(session, request.isbn)
            except RecordDoesNotExistError as exc:
                raise NotFound(str(exc)) from exc
            return Empty()

    def GetUser(
        self, request: pb.GetUserRequest, context: grpc.ServicerContext
    ) -> pb.UserDetail:
        """Get a user and books they have borrowed."""
        with grpc_dbsession() as session:
            try:
                user = get_user(session, request.email)
            except RecordDoesNotExistError as exc:
                raise NotFound(str(exc)) from exc
            return serialize_user(user)

    def ListBorrowedBooks(
        self, request: pb.ListGenericResourceRequest, context: grpc.ServicerContext
    ) -> pb.BookList:
        """List borrowed books in the library."""
        with grpc_dbsession() as session:
            results = list_books(
                session,
                is_available=False,
                page_num=request.page_num,
                page_size=request.page_size,
            )
            return pb.BookList(
                books=[
                    serialize_book(book, only_unavailable_copies=True)
                    for book in results.books
                ],
                metadata=serialize_paginator(
                    calculate_pagination_metadata(
                        results.nb_books,
                        page_size=request.page_size,
                        current_page=request.page_num,
                    )
                ),
            )

    def ListUsers(
        self, request: pb.ListGenericResourceRequest, context: grpc.ServicerContext
    ) -> pb.UserList:
        """List users enrolled in the library without books borrowed by each user."""

        with grpc_dbsession() as session:
            results = list_users(
                session, page_num=request.page_num, page_size=request.page_size
            )
            return pb.UserList(
                users=[serialize_user_without_books(user) for user in results.users],
                metadata=serialize_paginator(
                    calculate_pagination_metadata(
                        results.nb_users,
                        page_size=request.page_size,
                        current_page=request.page_num,
                    )
                ),
            )
