from datetime import timedelta
from uuid import uuid4

import pytest

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.token_sender import FakeTokenSender
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.user_gateway import FakeUserGateway
from tests.unit.access_service.application.interactors.const import (
    USER_EMAIL,
    USER_PASSWORD,
    USER_ID,
)
from zametka.access_service.domain.entities.config import (
    AccessTokenConfig,
    UserConfirmationTokenConfig,
)
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

from zametka.access_service.domain.entities.user import User


@pytest.fixture
def user_gateway() -> FakeUserGateway:
    return FakeUserGateway(
        User.create_with_raw_password(
            email=UserEmail(USER_EMAIL),
            raw_password=UserRawPassword(USER_PASSWORD),
            user_id=UserId(USER_ID),
        )
    )


@pytest.fixture
def id_provider(
    user_gateway: FakeUserGateway,
) -> FakeIdProvider:
    return FakeIdProvider(user_gateway.user)


@pytest.fixture
def uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


@pytest.fixture
def access_token_config() -> AccessTokenConfig:
    return AccessTokenConfig(expires_after=timedelta(days=30))


@pytest.fixture
def event_emitter() -> FakeEventEmitter:
    return FakeEventEmitter()


@pytest.fixture
def confirmation_token_config() -> UserConfirmationTokenConfig:
    return UserConfirmationTokenConfig(
        expires_after=timedelta(minutes=15),
    )


@pytest.fixture
def incorrect_confirmation_token(
    confirmation_token_config: UserConfirmationTokenConfig,
) -> UserConfirmationToken:
    return UserConfirmationToken(uid=UserId(uuid4()), config=confirmation_token_config)
