import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.models import User
from locallibrary_frontend.db.user import create_user, get_user_or_one


def test_user_does_not_exist(dbsession: OrmSession):
    """Check that no user exists on the database."""
    user = get_user_or_one(dbsession, "xyz@abc.com")
    assert user is None


def test_create_user(dbsession: OrmSession):
    email = "xyz@abc.com"
    first_name = "xyz"
    last_name = "abc"
    user = create_user(
        dbsession, email=email, first_name=first_name, last_name=last_name
    )
    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name


@pytest.mark.num_users(1)
def test_create_user_duplicate_email(dbsession: OrmSession, users: list[User]):
    existing_user = users[0]
    with pytest.raises(IntegrityError):
        create_user(
            dbsession,
            email=existing_user.email,
            last_name=existing_user.last_name,
            first_name=existing_user.first_name,
        )
