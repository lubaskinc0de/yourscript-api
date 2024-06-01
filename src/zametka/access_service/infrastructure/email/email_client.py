from abc import abstractmethod
from email.message import Message
from typing import Any, Protocol


class EmailClient(Protocol):
    @abstractmethod
    async def send(self, message: Message) -> Any: ...
