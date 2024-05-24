import aio_pika

from zametka.access_service.application.common.uow import UoW


class RabbitMQUoW(UoW):
    def __init__(self, rq_transaction: aio_pika.abc.AbstractTransaction) -> None:
        self._rq_transaction = rq_transaction

    async def commit(self) -> None:
        await self._rq_transaction.commit()

    async def rollback(self) -> None:
        await self._rq_transaction.rollback()

    async def flush(self) -> None:
        raise NotImplementedError
