from dataclasses import dataclass
from typing import Optional

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
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


class Authorize(Interactor[AuthorizeInputDTO, AccessToken]):
    def __init__(
        self,
        user_gateway: UserGateway,
        config: AccessTokenConfig,
    ):
        self.user_gateway = user_gateway
        self.config = config

    async def __call__(self, data: AuthorizeInputDTO) -> AccessToken:
        user: Optional[User] = await self.user_gateway.get_by_email(
            UserEmail(data.email)
        )

        if not user:
            raise UserIsNotExistsError()

        user.ensure_can_access()
        user.ensure_passwords_match(UserRawPassword(data.password))

        token = AccessToken(user.user_id, self.config)

        return token
