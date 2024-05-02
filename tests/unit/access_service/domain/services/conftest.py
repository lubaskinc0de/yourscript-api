from datetime import timedelta

import pytest

from tests.unit.access_service.domain.services.const import USER_PASSWORD
from tests.unit.access_service.domain.services.const import USER_EMAIL
from tests.unit.access_service.domain.services.const import USER_ID

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.services.token_access_service import TokenAccessService
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import UserRawPassword
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn

@pytest.fixture
def user() -> User:
    return User.create_with_raw_password(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_PASSWORD),
        user_id=UserId(USER_ID),
    )


@pytest.fixture
def access_token_config() -> AccessTokenConfig:
    return AccessTokenConfig(expires_after=timedelta(minutes=15))


@pytest.fixture
def access_token(user: User, access_token_config: AccessTokenConfig) -> AccessToken:
    return AccessToken(uid=user.user_id, config=access_token_config)


@pytest.fixture
def expired_access_token(user: User, access_token_config: AccessTokenConfig) -> AccessToken:
    token = AccessToken(uid=user.user_id, config=access_token_config)
    token._expires_in = ExpiresIn(token._expires_in.to_raw() - timedelta(days=1)) # noqa

    return token


@pytest.fixture
def token_access_service(access_token: AccessToken) -> TokenAccessService:
    return TokenAccessService(access_token)
