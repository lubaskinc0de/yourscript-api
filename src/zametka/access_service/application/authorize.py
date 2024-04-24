from dataclasses import dataclass
from typing import Optional

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import (
    UserGateway,
)

from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotExistsError,
)
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class AuthorizeInputDTO:
    email: str
    password: str


class Authorize(Interactor[AuthorizeInputDTO, UserDTO]):
    def __init__(
        self,
        user_gateway: UserGateway,
    ):
        self.user_gateway = user_gateway

    async def __call__(self, data: AuthorizeInputDTO) -> UserDTO:
        user: Optional[User] = await self.user_gateway.get_by_email(
            UserEmail(data.email)
        )

        if not user:
            raise UserIsNotExistsError()

        user.ensure_can_access()
        user.ensure_passwords_match(UserRawPassword(data.password))

        return UserDTO(
            user_id=user.user_id.to_raw(),
        )
