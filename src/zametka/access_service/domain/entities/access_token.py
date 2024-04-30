from zametka.access_service.domain.common.timed_user_token import TimedUserToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId


class AccessToken(TimedUserToken):
    def __init__(self, uid: UserId, config: AccessTokenConfig):
        self.uid = uid
        self._expires_in = ExpiresIn(self._now + config.expires_after)

    def verify(self) -> None:
        if self._is_expired:
            raise UnauthorizedError
        return None
