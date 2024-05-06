from datetime import timedelta, timezone, datetime
from uuid import uuid4

import argon2
import pytest

from zametka.access_service.domain.common.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.entities.config import (
    AccessTokenConfig,
    UserConfirmationTokenConfig,
)
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.services.password_hasher import (
    ArgonPasswordHasher,
    PasswordHasher,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@pytest.fixture
def access_token_config() -> AccessTokenConfig:
    return AccessTokenConfig(expires_after=timedelta(days=30))


@pytest.fixture
def confirmation_token_config() -> UserConfirmationTokenConfig:
    return UserConfirmationTokenConfig(
        expires_after=timedelta(minutes=15),
    )


@pytest.fixture
def user_email() -> UserEmail:
    return UserEmail("lubaskincorporation@gmail.com")


@pytest.fixture
def user_password() -> UserRawPassword:
    return UserRawPassword("someSuper123#Password")


@pytest.fixture
def user_id() -> UserId:
    return UserId(uuid4())


@pytest.fixture
def user_fake_id() -> UserId:
    return UserId(uuid4())


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return ArgonPasswordHasher(argon2.PasswordHasher())


@pytest.fixture
def user(
    password_hasher: PasswordHasher,
    user_email: UserEmail,
    user_password: UserRawPassword,
    user_id: UserId,
) -> User:
    return User.create_with_raw_password(
        email=user_email,
        raw_password=user_password,
        user_id=user_id,
        password_hasher=password_hasher,
    )


@pytest.fixture
def confirmation_token_expires_in(
    confirmation_token_config: UserConfirmationTokenConfig,
) -> ExpiresIn:
    expires_in = ExpiresIn(
        datetime.now(tz=timezone.utc) + confirmation_token_config.expires_after
    )
    return expires_in


@pytest.fixture
def confirmation_token(
    user: User, confirmation_token_expires_in: ExpiresIn
) -> UserConfirmationToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id, expires_in=confirmation_token_expires_in
    )
    token = UserConfirmationToken(metadata)
    return token


@pytest.fixture
def fake_confirmation_token(
    confirmation_token_expires_in: ExpiresIn,
    user_fake_id: UserId,
) -> UserConfirmationToken:
    metadata = TimedTokenMetadata(
        uid=user_fake_id, expires_in=confirmation_token_expires_in
    )
    token = UserConfirmationToken(metadata)
    return token


@pytest.fixture
def expired_confirmation_token(
    user: User, confirmation_token_config: UserConfirmationTokenConfig
):
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=ExpiresIn(
            datetime.now(tz=timezone.utc) - timedelta(days=1)
        ),
    )
    token = UserConfirmationToken(metadata)

    return token
