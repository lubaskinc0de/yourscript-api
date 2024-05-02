from typing import Protocol
from abc import abstractmethod

from zametka.access_service.domain.entities.user import User


class AccessService(Protocol):
    @abstractmethod
    def authorize(self, user: User) -> None: ...
