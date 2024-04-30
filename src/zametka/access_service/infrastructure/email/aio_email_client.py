from email.message import Message
from typing import Any

from aiosmtplib import SMTP

from zametka.access_service.infrastructure.email.email_client import EmailClient


class AioSMTPEmailClient(EmailClient):
    def __init__(self, aio_smtp_client: SMTP) -> None:
        self.client = aio_smtp_client

    async def send(self, message: Message) -> Any:
        async with self.client:
            await self.client.send_message(message)
