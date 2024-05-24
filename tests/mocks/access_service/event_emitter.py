from typing import Type

from zametka.access_service.application.common.event import (
    EventEmitter,
    EventsT,
    EventHandler,
)


class FakeEventEmitter(EventEmitter[EventsT]):
    def __init__(self) -> None:
        self._calls = dict()

    def on(self, event_type: Type[EventsT], handler: EventHandler[EventsT]) -> None:
        raise NotImplementedError

    def calls(self, event_type: Type[EventsT]):
        return event_type in self._calls

    async def emit(self, event: EventsT) -> None:
        if not self._calls.get(type(event)):
            self._calls[type(event)] = 1
        else:
            self._calls[type(event)] += 1
