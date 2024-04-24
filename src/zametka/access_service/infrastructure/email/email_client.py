from abc import abstractmethod
from typing import Protocol, Any

from zametka.access_service.infrastructure.email.email_message import EmailMessage


class EmailClient(Protocol):
    @abstractmethod
    async def send(self, message: EmailMessage) -> Any:
        ...
