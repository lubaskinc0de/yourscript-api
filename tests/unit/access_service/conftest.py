from datetime import UTC, datetime, timedelta
from uuid import uuid4

import argon2
import pytest
from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.common.value_objects.timed_token_id import (
    TimedTokenId,
)
from zametka.access_service.domain.entities.config import (
    AccessTokenConfig,
    UserConfirmationTokenConfig,
)
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)
from zametka.access_service.infrastructure.auth.password_hasher import (
    ArgonPasswordHasher,
)

EXPIRES_AFTER_MINUTES = 5


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
def token_expires_in() -> ExpiresIn:
    expires_in = ExpiresIn(
        datetime.now(tz=UTC) + timedelta(minutes=EXPIRES_AFTER_MINUTES),
    )
    return expires_in


@pytest.fixture
def token_expired_in(token_expires_in: ExpiresIn) -> ExpiresIn:
    return ExpiresIn(
        token_expires_in.to_raw() - timedelta(minutes=EXPIRES_AFTER_MINUTES + 1),
    )


@pytest.fixture
def confirmation_token(
    user: User,
    token_expires_in: ExpiresIn,
) -> UserConfirmationToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=token_expires_in,
    )
    token_id = TimedTokenId(uuid4())
    token = UserConfirmationToken(metadata, token_id)
    return token


@pytest.fixture
def fake_confirmation_token(
    token_expires_in: ExpiresIn,
    user_fake_id: UserId,
) -> UserConfirmationToken:
    metadata = TimedTokenMetadata(
        uid=user_fake_id,
        expires_in=token_expires_in,
    )
    token_id = TimedTokenId(uuid4())
    token = UserConfirmationToken(metadata, token_id)
    return token


@pytest.fixture
def expired_confirmation_token(
    user: User,
    confirmation_token_config: UserConfirmationTokenConfig,
):
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=ExpiresIn(datetime.now(tz=UTC) - timedelta(days=1)),
    )
    token_id = TimedTokenId(uuid4())
    token = UserConfirmationToken(metadata, token_id)
    return token
