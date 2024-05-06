import datetime
import pytest

from uuid import uuid4
from zametka.notes.domain.entities.user import User

from zametka.notes.domain.exceptions.user import (
    InvalidUserFirstNameError,
    InvalidUserLastNameError,
)
from zametka.notes.domain.value_objects.user.user_first_name import (
    UserFirstName,
)
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.notes.domain.value_objects.user.user_last_name import UserLastName


@pytest.mark.parametrize(
    "first_name",
    [
        "Ilya" * UserFirstName.MAX_LENGTH,
        "q" * (UserFirstName.MIN_LENGTH - 1),
        "",
        " ",
        "Ilya1",
    ],
)
def test_create_user_bad_first_name(first_name):
    with pytest.raises(InvalidUserFirstNameError):
        UserFirstName(first_name)


@pytest.mark.parametrize(
    "last_name",
    [
        "Lyubavski" * UserLastName.MAX_LENGTH,
        "q" * (UserLastName.MIN_LENGTH - 1),
        "",
        " ",
        "Lyubavski1",
    ],
)
def test_create_user_bad_last_name(last_name):
    with pytest.raises(InvalidUserLastNameError):
        UserLastName(last_name)


def test_read_joined_at():
    joined_at = UserJoinedAt(datetime.datetime.now())
    assert isinstance(joined_at.read(), datetime.date)


def test_create_user():
    user = User(
        first_name=UserFirstName("Ilya"),
        last_name=UserLastName("Lyubavski"),
        user_id=UserId(uuid4()),
    )

    assert user.joined_at
