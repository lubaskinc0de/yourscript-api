from typing import Callable, ClassVar, TypeVar, Generic, Any

from dataclasses import dataclass

from zametka.access_service.application.common.event import EventT
from zametka.access_service.infrastructure.event_bus.events.integration_event import (
    IntegrationEvent,
)


@dataclass(frozen=True, kw_only=True)
class AMQPEvent(IntegrationEvent[EventT], Generic[EventT]):
    exchange_name: ClassVar[str]
    routing_key: ClassVar[str]


EventType = TypeVar("EventType", bound=type[AMQPEvent[Any]])


def amqp_event(
    exchange: str,
    routing_key: str | None = None,
) -> Callable[[EventType], EventType]:
    def _amqp_event(cls: EventType) -> EventType:
        cls.exchange_name = exchange
        cls.routing_key = routing_key if routing_key is not None else cls.event_type
        return cls

    return _amqp_event
