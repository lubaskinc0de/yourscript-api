from dataclasses import dataclass
from uuid import UUID

from zametka.access_service.application.common.event.event import Event


@dataclass(frozen=True)
class UserDTO:
    user_id: UUID


@dataclass(frozen=True)
class UserDeletedEvent(Event):
    user_id: UUID
