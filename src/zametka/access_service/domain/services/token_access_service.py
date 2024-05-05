from zametka.access_service.domain.common.access_service import AccessService
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.access_token import (
    UnauthorizedError,
    AccessTokenIsExpiredError,
)
from zametka.access_service.domain.exceptions.user import UserIsNotActiveError


class TokenAccessService(AccessService):
    def __init__(self, token: AccessToken) -> None:
        self.token = token

    def authorize(self, user: User) -> None:
        try:
            user.ensure_is_active()
            self.token.verify()
        except (AccessTokenIsExpiredError, UserIsNotActiveError) as exc:
            raise exc from UnauthorizedError

        if not self.token.uid == user.user_id:
            raise UnauthorizedError
