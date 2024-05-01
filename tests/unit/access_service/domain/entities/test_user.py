import pytest

from datetime import timezone, datetime, timedelta
from uuid import uuid4

from zametka.access_service.domain.entities.config import UserConfirmationTokenConfig
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.confirmation_token import (
    CorruptedConfirmationTokenError,
    ConfirmationTokenAlreadyUsedError,
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    WeakPasswordError,
    InvalidUserEmailError,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

USER_EMAIL = "mockemail@gmail.com"
USER_FAKE_PASSWORD = "fake123Apassword##"


@pytest.fixture
def user() -> User:
    return User.create_with_raw_password(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_id=UserId(uuid4()),
    )


@pytest.fixture
def token(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
) -> UserConfirmationToken:
    return UserConfirmationToken(
        uid=user.user_id,
        config=confirmation_token_config,
    )


@pytest.mark.access
@pytest.mark.domain
def test_create_user(user: User):
    user.ensure_authenticated(UserRawPassword(USER_FAKE_PASSWORD))

    with pytest.raises(UserIsNotActiveError):
        user.ensure_can_authorize()

    assert user.hashed_password.to_raw() != USER_FAKE_PASSWORD


@pytest.mark.access
@pytest.mark.domain
def test_activate_user(user: User, token: UserConfirmationToken):
    user.activate(token)
    user.ensure_can_authorize()


@pytest.mark.access
@pytest.mark.domain
def test_activate_user_bad_uid(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
):
    fake_uid = uuid4()
    token = UserConfirmationToken(
        uid=UserId(fake_uid), config=confirmation_token_config
    )

    with pytest.raises(CorruptedConfirmationTokenError):
        user.activate(token)


@pytest.mark.access
@pytest.mark.domain
def test_activate_user_twice(user: User, token: UserConfirmationToken):
    user.activate(token)

    with pytest.raises(ConfirmationTokenAlreadyUsedError):
        user.activate(token)


@pytest.mark.access
@pytest.mark.domain
def test_activate_user_expired_token(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
):
    token = UserConfirmationToken.load(
        user.user_id,
        ExpiresIn(datetime.now(tz=timezone.utc) - timedelta(days=1)),
        confirmation_token_config,
    )

    with pytest.raises(ConfirmationTokenIsExpiredError):
        user.activate(token)


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
        "my.email@gmail.com",
    ],
)
def test_create_user_bad_email(email):
    with pytest.raises(InvalidUserEmailError):
        UserEmail(str(email))
