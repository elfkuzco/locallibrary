from fastapi import status
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    headers = {"Content-type": "application/json"}
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "jdoe@xyz.com",
    }

    response = client.post(
        "/users/create",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
