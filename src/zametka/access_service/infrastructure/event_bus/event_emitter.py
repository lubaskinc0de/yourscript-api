from typing import Optional, Type

from zametka.access_service.application.common.event import (
    EventEmitter,
    EventHandler,
    EventsT,
)


class EventEmitterImpl(EventEmitter[EventsT]):
    _events: dict[Type[EventsT], list[EventHandler[EventsT]]]

    def __init__(self) -> None:
        self._events = dict()

    def on(self, event_type: Type[EventsT], handler: EventHandler[EventsT]) -> None:
        existing_handlers = self._events.get(event_type)

        self._events[event_type] = (
            [handler] if not existing_handlers else existing_handlers + [handler]
        )

    async def emit(self, event: EventsT) -> None:
        handlers: Optional[list[EventHandler[EventsT]]] = self._events.get(type(event))

        if not handlers:
            return None

        for handler in handlers:
            await handler(event)
