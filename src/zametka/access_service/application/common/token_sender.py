from abc import abstractmethod

from typing import Protocol

from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.domain.entities.user import User


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    async def send(
        self, confirmation_token: UserConfirmationTokenDTO, user: User
    ) -> None:
        raise NotImplementedError
