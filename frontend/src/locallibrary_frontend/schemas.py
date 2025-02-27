import datetime
import math

import pydantic
from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )


class User(BaseModel):
    email: str
    id: str | None
    first_name: str | None
    last_name: str | None


class Paginator(BaseModel):
    total_records: int
    page_size: int
    current_page: int | None = None
    first_page: int | None = None
    last_page: int | None = None


class UserList(BaseModel):
    users: list[User]
    metadata: Paginator


class BookInstance(BaseModel):
    is_available: bool
    borrower_id: str | None = None
    due_date: datetime.datetime | None = None


class BookBase(BaseModel):
    isbn: str
    title: str
    summary: str | None = None
    created_at: datetime.datetime
    publisher_name: str
    categories: list[str]


class Book(BookBase):
    copies: list[BookInstance]


class BorrowBookRequest(BaseModel):
    email: str
    duration: int = Field(ge=30, le=1)


class BorrowedBook(BookBase, BookInstance):
    pass


class BookList(BaseModel):
    books: list[Book]
    metadata: Paginator


class RefreshToken(BaseModel):
    token: str | None
    provider: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthTokenStatus(BaseModel):
    is_valid: bool


def calculate_pagination_metadata(
    total_records: int, page_size: int, current_page: int
) -> Paginator:
    if total_records == 0:
        return Paginator(total_records=0, page_size=0)
    return Paginator(
        total_records=total_records,
        first_page=1,
        page_size=min(page_size, total_records),
        current_page=current_page,
        last_page=math.ceil(total_records / page_size),
    )
