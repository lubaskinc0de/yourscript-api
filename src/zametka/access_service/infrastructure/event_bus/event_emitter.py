from zametka.access_service.application.common.event import (
    EventEmitter,
    EventHandler,
    EventsT,
)


class EventEmitterImpl(EventEmitter[EventsT]):
    _events: dict[type[EventsT], list[EventHandler[EventsT]]]

    def __init__(self) -> None:
        self._events = {}

    def on(self, event_type: type[EventsT], handler: EventHandler[EventsT]) -> None:
        existing_handlers = self._events.get(event_type)

        if not existing_handlers:
            self._events[event_type] = [handler]
        else:
            self._events[event_type] = [handler, *existing_handlers]

    async def emit(self, event: EventsT) -> None:
        handlers: list[EventHandler[EventsT]] | None = self._events.get(type(event))

        if not handlers:
            return

        for handler in handlers:
            await handler(event)
