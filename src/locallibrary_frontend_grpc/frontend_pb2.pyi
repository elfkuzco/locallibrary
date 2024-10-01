from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddBookRequest(_message.Message):
    __slots__ = ("isbn", "title", "publisher_name", "categories", "summary")
    ISBN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    isbn: str
    title: str
    publisher_name: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    summary: str
    def __init__(self, isbn: _Optional[str] = ..., title: _Optional[str] = ..., publisher_name: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., summary: _Optional[str] = ...) -> None: ...

class RemoveBookRequest(_message.Message):
    __slots__ = ("isbn",)
    ISBN_FIELD_NUMBER: _ClassVar[int]
    isbn: str
    def __init__(self, isbn: _Optional[str] = ...) -> None: ...

class BookInstance(_message.Message):
    __slots__ = ("id", "borrower_id", "due_date", "is_available")
    ID_FIELD_NUMBER: _ClassVar[int]
    BORROWER_ID_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    borrower_id: str
    due_date: _timestamp_pb2.Timestamp
    is_available: bool
    def __init__(self, id: _Optional[str] = ..., borrower_id: _Optional[str] = ..., due_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_available: bool = ...) -> None: ...

class BookDetail(_message.Message):
    __slots__ = ("isbn", "title", "publisher_name", "created_at", "summary", "categories", "copies")
    ISBN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    COPIES_FIELD_NUMBER: _ClassVar[int]
    isbn: str
    title: str
    publisher_name: str
    created_at: _timestamp_pb2.Timestamp
    summary: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    copies: _containers.RepeatedCompositeFieldContainer[BookInstance]
    def __init__(self, isbn: _Optional[str] = ..., title: _Optional[str] = ..., publisher_name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., summary: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., copies: _Optional[_Iterable[_Union[BookInstance, _Mapping]]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class BorrowedBook(_message.Message):
    __slots__ = ("isbn", "title", "publisher_name", "created_at", "summary", "categories", "borrower_id", "due_date", "is_available")
    ISBN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    BORROWER_ID_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    isbn: str
    title: str
    publisher_name: str
    created_at: _timestamp_pb2.Timestamp
    summary: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    borrower_id: str
    due_date: _timestamp_pb2.Timestamp
    is_available: bool
    def __init__(self, isbn: _Optional[str] = ..., title: _Optional[str] = ..., publisher_name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., summary: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., borrower_id: _Optional[str] = ..., due_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_available: bool = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("email", "last_name", "first_name", "created_at")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    email: str
    last_name: str
    first_name: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, email: _Optional[str] = ..., last_name: _Optional[str] = ..., first_name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserDetail(_message.Message):
    __slots__ = ("email", "last_name", "first_name", "created_at", "borrowed_books")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    BORROWED_BOOKS_FIELD_NUMBER: _ClassVar[int]
    email: str
    last_name: str
    first_name: str
    created_at: _timestamp_pb2.Timestamp
    borrowed_books: _containers.RepeatedCompositeFieldContainer[BorrowedBook]
    def __init__(self, email: _Optional[str] = ..., last_name: _Optional[str] = ..., first_name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., borrowed_books: _Optional[_Iterable[_Union[BorrowedBook, _Mapping]]] = ...) -> None: ...

class ListGenericResourceRequest(_message.Message):
    __slots__ = ("page_size", "page_num")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_num: int
    def __init__(self, page_size: _Optional[int] = ..., page_num: _Optional[int] = ...) -> None: ...

class Paginator(_message.Message):
    __slots__ = ("total_records", "page_size", "current_page", "first_page", "last_page")
    TOTAL_RECORDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PAGE_FIELD_NUMBER: _ClassVar[int]
    FIRST_PAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_PAGE_FIELD_NUMBER: _ClassVar[int]
    total_records: int
    page_size: int
    current_page: int
    first_page: int
    last_page: int
    def __init__(self, total_records: _Optional[int] = ..., page_size: _Optional[int] = ..., current_page: _Optional[int] = ..., first_page: _Optional[int] = ..., last_page: _Optional[int] = ...) -> None: ...

class BookList(_message.Message):
    __slots__ = ("books", "metadata")
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[BookDetail]
    metadata: Paginator
    def __init__(self, books: _Optional[_Iterable[_Union[BookDetail, _Mapping]]] = ..., metadata: _Optional[_Union[Paginator, _Mapping]] = ...) -> None: ...

class UserList(_message.Message):
    __slots__ = ("users", "metadata")
    USERS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    metadata: Paginator
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., metadata: _Optional[_Union[Paginator, _Mapping]] = ...) -> None: ...
