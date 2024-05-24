from abc import ABC, abstractmethod
from typing import Generic, Type

from zametka.access_service.application.common.event.event_handler import (
    EventHandler,
)
from zametka.access_service.application.common.event.event import EventsT


class EventEmitter(Generic[EventsT], ABC):
    @abstractmethod
    def on(self, event_type: Type[EventsT], handler: EventHandler[EventsT]) -> None: ...

    @abstractmethod
    async def emit(self, event: EventsT) -> None: ...
