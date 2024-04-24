import pytest

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
    EXPIRES_AFTER,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@pytest.fixture
def user() -> User:
    return User.create_with_raw_password(
        email=UserEmail("testemail@gmail.com"),
        raw_password=UserRawPassword("fakePassword12#@"),
        user_id=UserId(uuid4()),
    )


@pytest.mark.access
@pytest.mark.domain
def test_create_token(user: User):
    token = UserConfirmationToken(
        uid=user.user_id,
    )

    token.verify()


@pytest.mark.access
@pytest.mark.domain
def test_verify_expired_token(user: User):
    expires = datetime.now(tz=timezone.utc) - timedelta(days=EXPIRES_AFTER.days + 5)
    token = UserConfirmationToken.load(user.user_id, expires)

    with pytest.raises(ConfirmationTokenIsExpiredError):
        token.verify()
