from zametka.access_service.application.common.event import (
    EventEmitter,
    EventHandler,
    EventsT,
)


class FakeEventEmitter(EventEmitter[EventsT]):
    def __init__(self) -> None:
        self._calls = {}

    def on(self, event_type: type[EventsT], handler: EventHandler[EventsT]) -> None:
        raise NotImplementedError

    def calls(self, event_type: type[EventsT]):
        return event_type in self._calls

    async def emit(self, event: EventsT) -> None:
        if not self._calls.get(type(event)):
            self._calls[type(event)] = 1
        else:
            self._calls[type(event)] += 1
