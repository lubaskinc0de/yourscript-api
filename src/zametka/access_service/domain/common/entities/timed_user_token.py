from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from zametka.access_service.domain.common.value_objects.timed_token_id import (
    TimedTokenId,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class TimedTokenMetadata:
    uid: UserId
    expires_in: ExpiresIn


@dataclass(frozen=True)
class TimedUserToken(ABC):
    metadata: TimedTokenMetadata
    token_id: TimedTokenId

    @property
    def expires_in(self) -> ExpiresIn:
        return self.metadata.expires_in

    @property
    def uid(self) -> UserId:
        return self.metadata.uid

    @abstractmethod
    def verify(self) -> None: ...
