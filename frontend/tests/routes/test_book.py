import pytest
from fastapi import status
from fastapi.testclient import TestClient

from locallibrary_frontend.db.models import Book
from locallibrary_frontend.serializers import serialize_book


def test_book_does_not_exist(client: TestClient):
    """Check that book does not exist."""
    headers = {"Content-type": "application/json"}
    response = client.get(
        "/books/doesnotexist",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.num_books(1)
def test_get_book(client: TestClient, books: list[Book]):
    """Check that books can be fetched by isbn."""
    headers = {"Content-type": "application/json"}
    book = books[0]
    response = client.get(
        f"/books/{book.isbn}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert serialize_book(book).model_dump(by_alias=True, mode="json") == data


@pytest.mark.num_books(100)
def test_tests_list(client: TestClient, books: list[Book]):
    response = client.get("/books")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "metadata" in data
    assert "books" in data
    metadata = data["metadata"]
    assert metadata["totalRecords"] == len(books)
