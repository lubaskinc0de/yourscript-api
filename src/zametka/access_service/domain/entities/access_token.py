from datetime import datetime, timezone

from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.value_objects.user_id import UserId


class AccessToken:
    __slots__ = ("uid", "_expires_in")

    def __init__(self, uid: UserId, config: AccessTokenConfig):
        self.uid = uid

        timestamp = datetime.now(tz=timezone.utc)
        self._expires_in = timestamp + config.expires_after

    @classmethod
    def load(
        cls, uid: UserId, expires_in: datetime, config: AccessTokenConfig
    ) -> "AccessToken":
        instance = cls(uid, config)
        instance._expires_in = expires_in

        return instance

    @property
    def expires_in(self):
        return self._expires_in

    def verify(self) -> None:
        now = datetime.now(tz=timezone.utc)

        if now > self._expires_in:
            raise UnauthorizedError

        return None
