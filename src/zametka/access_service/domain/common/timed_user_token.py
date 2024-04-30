from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Self, Type

from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId


class TimedUserToken(ABC):
    __slots__ = ("uid", "_expires_in")

    uid: UserId
    _expires_in: ExpiresIn

    @classmethod
    def load(
        cls: Type[Self], uid: UserId, expires_in: ExpiresIn, *args, **kwargs
    ) -> Self:
        instance = cls(uid, *args, **kwargs)
        instance._expires_in = expires_in

        return instance

    @property
    def expires_in(self) -> ExpiresIn:
        return self._expires_in

    @property
    def _is_expired(self) -> bool:
        if self._expires_in.is_expired:
            return True
        return False

    @property
    def _now(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    @abstractmethod
    def verify(self) -> None: ...
