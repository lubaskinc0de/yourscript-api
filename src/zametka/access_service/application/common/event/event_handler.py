import logging

from abc import ABC
from typing import Generic

from zametka.access_service.application.common.event.event import EventT


class EventHandler(Generic[EventT], ABC):
    async def __call__(self, event: EventT) -> None:
        logging.info("Handling event: %s", event)
