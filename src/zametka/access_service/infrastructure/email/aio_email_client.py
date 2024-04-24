from email.message import EmailMessage as SMTPMessage
from typing import Any

from aiosmtplib import SMTP

from zametka.access_service.infrastructure.email.email_client import EmailClient
from zametka.access_service.infrastructure.email.email_message import EmailMessage


class AioSMTPEmailClient(EmailClient):
    def __init__(self, aio_smtp_client: SMTP) -> None:
        self.client = aio_smtp_client

    async def send(self, message: EmailMessage) -> Any:
        async with self.client:
            smtp_message = SMTPMessage()

            smtp_message["From"] = message.email_from
            smtp_message["To"] = message.email_to
            smtp_message["Subject"] = message.subject
            smtp_message.set_content(message.content)

            await self.client.send_message(smtp_message)
