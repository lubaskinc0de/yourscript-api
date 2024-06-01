from uuid import uuid4

import pytest
from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.common.value_objects.timed_token_id import (
    TimedTokenId,
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
    token_expires_in: ExpiresIn,
) -> AccessToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=token_expires_in,
    )
    token_id = TimedTokenId(uuid4())
    return AccessToken(metadata, token_id)


@pytest.fixture
def expired_access_token(
    user: User,
    token_expired_in: ExpiresIn,
) -> AccessToken:
    metadata = TimedTokenMetadata(
        uid=user.user_id,
        expires_in=token_expired_in,
    )

    token_id = TimedTokenId(uuid4())
    token = AccessToken(metadata, token_id=token_id)

    return token


@pytest.fixture
def token_access_service(access_token: AccessToken) -> TokenAccessService:
    return TokenAccessService(access_token)
