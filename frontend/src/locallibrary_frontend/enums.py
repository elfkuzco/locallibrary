from enum import StrEnum


class UserSortColumnEnum(StrEnum):
    """Fields for sorting users from a database"""

    email = "email"
    created_at = "created_at"
    first_name = "first_name"
    last_name = "last_name"


class BookSortColumnEnum(StrEnum):
    """Fields for sorting books from a database"""

    created_at = "created_at"
    isbn = "isbn"


class SortDirectionEnum(StrEnum):
    """Direction to sort list of results from a database"""

    asc = "asc"
    desc = "desc"
