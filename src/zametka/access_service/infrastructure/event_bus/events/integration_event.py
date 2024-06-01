from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar
from uuid import UUID, uuid4

from zametka.access_service.application.common.event import Event, EventT


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent(Event, Generic[EventT]):
    event_id: UUID = field(default_factory=uuid4)
    event_timestamp: datetime = field(default_factory=datetime.utcnow)
    event_type: ClassVar[str]
    original_event: EventT


EventType = TypeVar("EventType", bound=type[IntegrationEvent[Any]])


def integration_event(
    event_type: str,
) -> Callable[[EventType], EventType]:
    def _integration_event(cls: EventType) -> EventType:
        cls.event_type = event_type
        return cls

    return _integration_event
