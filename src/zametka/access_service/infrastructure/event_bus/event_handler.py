from zametka.access_service.application.common.event import (
    EventHandler,
)
from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.infrastructure.event_bus.amqp_event_sender import (
    AMQPEventSender,
)
from zametka.access_service.infrastructure.event_bus.events import (
    AMQPEvent,
    UserDeletedAMQPEvent,
)


class UserDeletedEventHandler(EventHandler[UserDeletedEvent]):
    def __init__(self, event_sender: AMQPEventSender) -> None:
        self.event_sender = event_sender

    async def __call__(self, event: UserDeletedEvent) -> None:
        await super().__call__(event)

        amqp_event: AMQPEvent[UserDeletedEvent] = UserDeletedAMQPEvent(
            original_event=event,
        )

        await self.event_sender.send(amqp_event)
