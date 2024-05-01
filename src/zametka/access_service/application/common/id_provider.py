from abc import abstractmethod
from typing import Protocol

from zametka.access_service.domain.entities.user import User


class IdProvider(Protocol):
    @abstractmethod
    async def get_user(self) -> User:
        ...
