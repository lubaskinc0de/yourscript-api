from dataclasses import dataclass

from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.infrastructure.event_bus.exchanges import (
    USER_EXCHANGE,
)

from .amqp_event import AMQPEvent, amqp_event
from .integration_event import integration_event


@dataclass(frozen=True)
@amqp_event(exchange=USER_EXCHANGE)
@integration_event("UserDeletedEvent")
class UserDeletedAMQPEvent(AMQPEvent[UserDeletedEvent]):
    pass
