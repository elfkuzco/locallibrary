import pytest
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.exceptions import RecordDoesNotExistError
from locallibrary_frontend.db.models import User
from locallibrary_frontend.db.user import create_user, get_user


def test_user_does_not_exist(dbsession: OrmSession):
    """Check that no user exists on the database."""
    with pytest.raises(RecordDoesNotExistError):
        get_user(dbsession, "xyz@abc.com")


def test_create_user(dbsession: OrmSession):
    """Check that we create a user."""
    email = "xyz@abc.com"
    first_name = "xyz"
    last_name = "abc"
    user_id = "1234568"
    user = create_user(
        dbsession,
        email=email,
        first_name=first_name,
        last_name=last_name,
        user_id=user_id,
    )
    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.id == user_id


@pytest.mark.num_users(1)
def test_get_user(dbsession: OrmSession, users: list[User]):
    """Check that we can get a user."""
    existing_user = users[0]
    db_user = get_user(
        dbsession, existing_user.id  # pyright: ignore[reportArgumentType]
    )
    assert db_user.email == existing_user.email
    assert db_user.last_name == existing_user.last_name
    assert db_user.first_name == existing_user.first_name
