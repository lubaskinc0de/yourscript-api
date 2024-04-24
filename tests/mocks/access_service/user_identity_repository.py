from typing import Optional

from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId


class FakeUserGateway(UserGateway):
    def __init__(self, user: User):
        self.user = user
        self.created = False
        self.updated = False
        self.deleted = False

    async def create(self, user: User) -> UserDTO:
        self.created = True
        return UserDTO(
            user_id=self.user.user_id.to_raw(),
        )

    async def get(self, user_id: UserId) -> Optional[User]:
        if not self.user.user_id == user_id:
            return None

        return self.user

    async def get_by_email(self, email: UserEmail) -> Optional[User]:
        if not self.user.email == email:
            return None

        return self.user

    async def update(self, user_id: UserId, updated_user: User) -> None:
        self.updated = True

        self.user.is_active = updated_user.is_active
        self.user.email = updated_user.email
        self.user.hashed_password = updated_user.hashed_password
        self.user.user_id = updated_user.user_id

    async def delete(self, user_id: UserId) -> None:
        self.deleted = True
