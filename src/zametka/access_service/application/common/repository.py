from abc import abstractmethod
from typing import Optional, Protocol

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId


class UserGateway(Protocol):
    @abstractmethod
    async def create(self, user: User) -> UserDTO:
        """Create"""

    @abstractmethod
    async def get(self, user_id: UserId) -> Optional[User]:
        """Get by id"""

    @abstractmethod
    async def get_by_email(self, email: UserEmail) -> Optional[User]:
        """Get by email"""

    @abstractmethod
    async def update(self, user_id: UserId, updated_user: User) -> None:
        """Update"""

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete"""
