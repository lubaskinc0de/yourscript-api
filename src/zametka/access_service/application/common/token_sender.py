from abc import abstractmethod

from typing import Protocol

from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    async def send(self, confirmation_token: UserConfirmationToken, user: User) -> None:
        raise NotImplementedError
