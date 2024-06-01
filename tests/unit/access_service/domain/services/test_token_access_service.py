from uuid import uuid4

import pytest
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from zametka.access_service.domain.exceptions.user import UserIsNotActiveError
from zametka.access_service.domain.services.token_access_service import (
    TokenAccessService,
)


@pytest.mark.access
@pytest.mark.domain
def test_authorize(token_access_service: TokenAccessService, user: User):
    user.is_active = True
    token_access_service.authorize(user)


@pytest.mark.access
@pytest.mark.domain
def test_authorize_not_active(token_access_service: TokenAccessService, user: User):
    with pytest.raises(UserIsNotActiveError):
        token_access_service.authorize(user)


@pytest.mark.access
@pytest.mark.domain
def test_authorize_expired_token(expired_access_token: AccessToken, user: User):
    token_access_service = TokenAccessService(expired_access_token)
    user.is_active = True

    with pytest.raises(AccessTokenIsExpiredError):
        token_access_service.authorize(user)


@pytest.mark.access
@pytest.mark.domain
def test_authorize_bad_user(token_access_service: TokenAccessService, user: User):
    user.user_id = uuid4()
    user.is_active = True

    with pytest.raises(UnauthorizedError):
        token_access_service.authorize(user)
