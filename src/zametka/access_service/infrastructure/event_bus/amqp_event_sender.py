import logging

from typing import Any
from adaptix import Retort

from zametka.access_service.infrastructure.event_bus.events import AMQPEvent
from zametka.access_service.infrastructure.message_broker.interface import MessageBroker
from zametka.access_service.infrastructure.message_broker.message import Message


class AMQPEventSender:
    def __init__(self, retort: Retort, message_broker: MessageBroker) -> None:
        self._retort = retort
        self._message_broker = message_broker

    async def send(self, event: AMQPEvent[Any]) -> None:
        original_event = event.original_event
        message_data = self._retort.dump(original_event)

        broker_message = Message(
            message_id=event.event_id,
            data=message_data,
        )

        await self._message_broker.publish_message(
            broker_message, event.routing_key, event.exchange_name
        )

        logging.info("Event %s was published.", event)
