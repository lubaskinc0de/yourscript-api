import pytest

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from zametka.access_service.domain.entities.config import UserConfirmationTokenConfig
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
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
def test_create_token(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
):
    token = UserConfirmationToken(
        uid=user.user_id,
        config=confirmation_token_config,
    )

    token.verify()


@pytest.mark.access
@pytest.mark.domain
def test_verify_expired_token(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
):
    expires = datetime.now(tz=timezone.utc) - (
        timedelta(days=1) + confirmation_token_config.expires_after
    )
    token = UserConfirmationToken.load(
        user.user_id, ExpiresIn(expires), confirmation_token_config
    )

    with pytest.raises(ConfirmationTokenIsExpiredError):
        token.verify()
