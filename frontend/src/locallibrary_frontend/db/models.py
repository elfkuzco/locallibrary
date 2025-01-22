from __future__ import annotations

import datetime
from uuid import UUID

from sqlalchemy import (
    BIGINT,
    ForeignKey,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.types import ARRAY, TIMESTAMP


class Base(MappedAsDataclass, DeclarativeBase):
    # This map details the specific transformation of types between Python and
    # PostgreSQL. This is only needed for the case where a specific PostgreSQL
    # type has to be used.

    type_annotation_map = {  # noqa
        str: CITEXT,  # use case-insensitive text on PostgreSQL backend
        int: BIGINT,
        list[str]: ARRAY(item_type=CITEXT),
        datetime.datetime: TIMESTAMP(
            timezone=True
        ),  # make datetimes to be timezone-aware
    }

    # This metadata specifies some naming conventions that will be used by
    # alembic to generate constraints names (indexes, unique constraints, ...)
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    pass


class User(Base):
    """Model representing users of the library."""

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(primary_key=True)
    id: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        init=False,
    )
    borrowed_books: Mapped[list[BookInstance]] = relationship(
        primaryjoin=(
            "and_"
            "(User.email==BookInstance.borrower_id, "
            "BookInstance.is_available==False)"
        ),
        back_populates="borrower",
        init=False,
        repr=False,
    )
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
        init=False,
        repr=False,
    )

    __table_args__ = (UniqueConstraint("id"),)


class RefreshToken(Base):
    """Model representing refresh tokens from various providers."""

    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, init=False, repr=False
    )
    refresh_token: Mapped[str]
    provider: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
    user: Mapped[User] = relationship(
        back_populates="refresh_tokens", init=False, repr=False
    )


class BookCategory(Base):
    """Association table for many-to-many relationships between book and category."""

    __tablename__ = "book_category"
    book_isbn: Mapped[str] = mapped_column(ForeignKey("book.isbn"), primary_key=True)
    category_name: Mapped[str] = mapped_column(
        ForeignKey("category.name"), primary_key=True
    )


class Category(Base):
    """Model representing book category."""

    __tablename__ = "category"

    name: Mapped[str] = mapped_column(primary_key=True)
    books: Mapped[list[Book]] = relationship(
        back_populates="categories",
        init=False,
        secondary=BookCategory.__table__,
        repr=False,
    )


class Publisher(Base):
    """Model representing a book publisher."""

    __tablename__ = "publisher"

    name: Mapped[str] = mapped_column(primary_key=True)
    books: Mapped[list[Book]] = relationship(
        back_populates="publisher", init=False, repr=False
    )


class Book(Base):
    """Model representing a book (but not a specific copy of a book)"""

    __tablename__ = "book"

    isbn: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    summary: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        init=False,
    )
    publisher_name: Mapped[str] = mapped_column(
        ForeignKey("publisher.name"), init=False
    )

    categories: Mapped[list[Category]] = relationship(
        back_populates="books",
        init=False,
        secondary=BookCategory.__table__,
        repr=False,
    )

    publisher: Mapped[Publisher] = relationship(
        back_populates="books", init=False, repr=False
    )
    instances: Mapped[list[BookInstance]] = relationship(
        back_populates="book",
        cascade="all, delete",
        passive_deletes=True,
        init=False,
        repr=False,
    )
    borrowed_instances: Mapped[list[BookInstance]] = relationship(
        primaryjoin=(
            "and_"
            "(Book.isbn==BookInstance.book_isbn, "
            "BookInstance.is_available==False)"
        ),
        init=False,
        repr=False,
        viewonly=True,
    )


class BookInstance(Base):
    """Model representing a specific copy of book."""

    __tablename__ = "book_instance"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    due_date: Mapped[datetime.datetime | None] = mapped_column(default=None)
    is_available: Mapped[bool] = mapped_column(default=True)
    book_isbn: Mapped[str] = mapped_column(
        ForeignKey("book.isbn", ondelete="CASCADE"), init=False
    )
    borrower_id: Mapped[str | None] = mapped_column(
        ForeignKey("user.email"), init=False, default=None
    )

    book: Mapped[Book] = relationship(
        back_populates="instances", init=False, repr=False
    )
    borrower: Mapped[User | None] = relationship(
        back_populates="borrowed_books", init=False, repr=False, default=None
    )
