from datetime import timedelta

import pytest

from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedTokenMetadata,
)

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.services.token_access_service import (
    TokenAccessService,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn


@pytest.fixture
def access_token(
    user: User,
    confirmation_token_expires_in: ExpiresIn,
) -> AccessToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id, expires_in=confirmation_token_expires_in
    )
    return AccessToken(metadata)


@pytest.fixture
def expired_access_token(
    user: User, confirmation_token_expires_in: ExpiresIn
) -> AccessToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=ExpiresIn(
            confirmation_token_expires_in.to_raw() - timedelta(days=1)
        ),
    )
    token = AccessToken(metadata)

    return token


@pytest.fixture
def token_access_service(access_token: AccessToken) -> TokenAccessService:
    return TokenAccessService(access_token)
