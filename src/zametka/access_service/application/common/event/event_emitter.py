from abc import ABC, abstractmethod
from typing import Generic

from zametka.access_service.application.common.event.event import EventsT
from zametka.access_service.application.common.event.event_handler import (
    EventHandler,
)


class EventEmitter(Generic[EventsT], ABC):
    @abstractmethod
    def on(self, event_type: type[EventsT], handler: EventHandler[EventsT]) -> None: ...

    @abstractmethod
    async def emit(self, event: EventsT) -> None: ...
