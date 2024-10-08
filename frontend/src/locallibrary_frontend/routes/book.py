import datetime
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi import status as status_codes

from locallibrary_frontend.db.books import borrow_book as db_borrow_book
from locallibrary_frontend.db.books import get_available_book_instances
from locallibrary_frontend.db.books import get_book as db_get_book
from locallibrary_frontend.db.books import list_books as db_list_books
from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.user import get_user
from locallibrary_frontend.enums import (
    BookSortColumnEnum,
    SortDirectionEnum,
)
from locallibrary_frontend.routes.dependencies import DbSession
from locallibrary_frontend.routes.http_errors import NotFoundError
from locallibrary_frontend.schemas import (
    Book,
    BookList,
    BorrowBookRequest,
    BorrowedBook,
    calculate_pagination_metadata,
)
from locallibrary_frontend.serializers import serialize_book, serialize_borrowed_book
from locallibrary_frontend.settings import Settings

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "",
    status_code=status_codes.HTTP_200_OK,
    responses={
        status_codes.HTTP_200_OK: {"description": "Returns the list of books."},
    },
)
def list_books(
    session: DbSession,
    page_size: Annotated[
        int, Query(le=Settings.MAX_PAGE_SIZE, ge=1)
    ] = Settings.MAX_PAGE_SIZE,
    category: Annotated[str | None, Query()] = None,
    publishers: Annotated[list[str] | None, Query()] = None,
    is_available: Annotated[bool | None, Query()] = None,
    page_num: Annotated[int, Query(ge=1)] = 1,
    sort_by: Annotated[BookSortColumnEnum, Query()] = BookSortColumnEnum.created_at,
    order: Annotated[SortDirectionEnum, Query()] = SortDirectionEnum.asc,
) -> BookList:
    result = db_list_books(
        session,
        category=category,
        publishers=publishers,
        page_size=page_size,
        page_num=page_num,
        is_available=is_available,
        sort_column=sort_by,
        sort_direction=order,
    )
    return BookList(
        books=[serialize_book(book) for book in result.books],
        metadata=calculate_pagination_metadata(
            result.nb_books, page_size=page_size, current_page=page_num
        ),
    )


@router.get(
    "/{isbn}",
    status_code=status_codes.HTTP_200_OK,
    responses={
        status_codes.HTTP_200_OK: {"description": "Returns the book with isbn."},
    },
)
def get_book(isbn: Annotated[str, Path()], session: DbSession) -> Book:
    try:
        book = db_get_book(session, isbn)
    except RecordDoesNotExistError as exc:
        raise NotFoundError(str(exc)) from exc
    return serialize_book(book)


@router.post(
    "/borrow/{isbn}",
    status_code=status_codes.HTTP_200_OK,
    responses={
        status_codes.HTTP_200_OK: {"description": "Borrowed book successfully"},
    },
)
def borrow_book(
    isbn: Annotated[str, Path()], request: BorrowBookRequest, session: DbSession
) -> BorrowedBook:
    try:
        user = get_user(session, request.email)
    except RecordDoesNotExistError as exc:
        raise NotFoundError(str(exc)) from exc

    available_copies = get_available_book_instances(session, isbn)
    if not available_copies:
        raise NotFoundError("The book is not available at the moment.")

    borrowed_book = db_borrow_book(
        session,
        user,
        available_copies[0],
        datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=request.duration),
    )
    return serialize_borrowed_book(borrowed_book)
