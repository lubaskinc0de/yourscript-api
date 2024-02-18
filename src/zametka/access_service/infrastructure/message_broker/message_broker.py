import json
import logging
import aio_pika

from aio_pika.abc import AbstractChannel

from .interface import MessageBroker
from .message import Message


class MessageBrokerImpl(MessageBroker):
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        rq_message = aio_pika.Message(
            body=json.dumps(
                dict(message_type=message.message_type, data=message.data)
            ).encode(),
            message_id=str(message.message_id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers={},
        )

        await self._publish_message(rq_message, routing_key, exchange_name)

    async def declare_exchange(self, exchange_name: str) -> None:
        await self._channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)

    async def _publish_message(
        self,
        rq_message: aio_pika.Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        exchange = await self._get_exchange(exchange_name)
        await exchange.publish(rq_message, routing_key=routing_key)

        logging.debug("Message sent", extra={"rq_message": rq_message})

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self._channel.get_exchange(exchange_name, ensure=False)
