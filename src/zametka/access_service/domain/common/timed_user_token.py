from __future__ import annotations

from abc import abstractmethod, ABC
from dataclasses import dataclass

from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class TimedTokenMetadata:
    uid: UserId
    expires_in: ExpiresIn


class TimedUserToken(ABC):
    __slots__ = ("metadata",)

    metadata: TimedTokenMetadata

    def __init__(self, metadata: TimedTokenMetadata) -> None:
        self.metadata = metadata

    @property
    def expires_in(self) -> ExpiresIn:
        return self.metadata.expires_in

    @property
    def uid(self) -> UserId:
        return self.metadata.uid

    @abstractmethod
    def verify(self) -> None: ...
