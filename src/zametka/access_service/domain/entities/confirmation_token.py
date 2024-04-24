from datetime import datetime, timedelta, timezone

from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.value_objects.user_id import UserId

EXPIRES_AFTER = timedelta(minutes=15)


class UserConfirmationToken:
    __slots__ = ("uid", "_expires_in")

    def __init__(self, uid: UserId):
        self.uid = uid
        self._expires_in = datetime.now(tz=timezone.utc) + EXPIRES_AFTER

    @classmethod
    def load(
        cls, uid: UserId, timestamp: datetime
    ) -> "UserConfirmationToken":
        uid = uid
        expires_in = timestamp + EXPIRES_AFTER

        instance = cls(uid)
        instance._expires_in = expires_in

        return instance

    def verify(self) -> None:
        now = datetime.now(tz=timezone.utc)

        if now > self._expires_in:
            raise ConfirmationTokenIsExpiredError

        return None
