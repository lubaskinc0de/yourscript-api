from typing import Optional

from zametka.access_service.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId


class FakeUserGateway(UserReader, UserSaver):
    def __init__(self, user: User):
        self.user = user
        self.saved = False
        self.deleted = False

    async def save(self, user: User) -> UserDTO:
        self.user.is_active = user.is_active
        self.user.email = user.email
        self.user.hashed_password = user.hashed_password

        self.saved = True

        return UserDTO(
            user_id=self.user.user_id.to_raw(),
        )

    async def with_id(self, user_id: UserId) -> Optional[User]:
        if not self.user.user_id == user_id:
            return None

        return self.user

    async def with_email(self, email: UserEmail) -> Optional[User]:
        if not self.user.email == email:
            return None

        return self.user

    async def delete(self, user_id: UserId) -> None:
        self.deleted = True
