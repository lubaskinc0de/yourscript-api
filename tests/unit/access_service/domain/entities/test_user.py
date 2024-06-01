import pytest
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenAlreadyUsedError,
    ConfirmationTokenIsExpiredError,
    CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.exceptions.user import (
    InvalidUserEmailError,
    UserIsNotActiveError,
    WeakPasswordError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@pytest.mark.access
@pytest.mark.domain
def test_create_user(
    user: User,
    password_hasher: PasswordHasher,
    user_password: UserRawPassword,
):
    user.authenticate(user_password, password_hasher)

    with pytest.raises(UserIsNotActiveError):
        user.ensure_is_active()

    assert user.hashed_password.to_raw() != user_password.to_raw()


@pytest.mark.access
@pytest.mark.domain
def test_activate_user(user: User, confirmation_token: UserConfirmationToken):
    user.activate(confirmation_token)
    user.ensure_is_active()


@pytest.mark.access
@pytest.mark.domain
@pytest.mark.parametrize(
    ["exc_class", "fixture_name"],
    [
        (CorruptedConfirmationTokenError, "fake_confirmation_token"),
        (ConfirmationTokenIsExpiredError, "expired_confirmation_token"),
    ],
)
def test_activate_user_bad_token(exc_class, fixture_name, user: User, request):
    token = request.getfixturevalue(fixture_name)
    with pytest.raises(exc_class):
        user.activate(token)


@pytest.mark.access
@pytest.mark.domain
def test_activate_user_twice(user: User, confirmation_token: UserConfirmationToken):
    user.activate(confirmation_token)

    with pytest.raises(ConfirmationTokenAlreadyUsedError):
        user.activate(confirmation_token)


@pytest.mark.access
@pytest.mark.domain
@pytest.mark.parametrize(
    "pwd",
    [
        "qwerty",
        "qwertyA",
        "qwertyA1",
    ],
)
def test_create_user_bad_password(pwd):
    with pytest.raises(WeakPasswordError):
        UserRawPassword(pwd)


@pytest.mark.access
@pytest.mark.domain
@pytest.mark.parametrize(
    "email",
    [
        "abc",
        "a" * 120,
        "myawesomeemail@gmail",
        "............@gmail.com",
        "myemailgmail.com",
        "my email@gmail.com",
        "              ",
        12345,
    ],
)
def test_create_user_bad_email(email):
    with pytest.raises(InvalidUserEmailError):
        UserEmail(str(email))
