from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from zametka.access_service.application.common.exceptions.user import (
    UserIsNotExistsError,
)
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.user_gateway import UserReader
from zametka.access_service.application.dto import AccessTokenDTO
from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.common.value_objects.timed_token_id import (
    TimedTokenId,
)
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class AuthorizeInputDTO:
    email: str
    password: str


class Authorize(Interactor[AuthorizeInputDTO, AccessTokenDTO]):
    def __init__(
        self,
        user_gateway: UserReader,
        config: AccessTokenConfig,
        password_hasher: PasswordHasher,
    ):
        self.user_gateway = user_gateway
        self.config = config
        self.ph = password_hasher

    async def __call__(self, data: AuthorizeInputDTO) -> AccessTokenDTO:
        user: User | None = await self.user_gateway.with_email(UserEmail(data.email))

        if not user:
            raise UserIsNotExistsError()

        user.authenticate(UserRawPassword(data.password), self.ph)
        user.ensure_is_active()

        now = datetime.now(tz=UTC)
        expires_in = ExpiresIn(now + self.config.expires_after)
        metadata = TimedTokenMetadata(uid=user.user_id, expires_in=expires_in)

        token_id = TimedTokenId(uuid4())
        token = AccessToken(metadata, token_id=token_id)

        return AccessTokenDTO(
            uid=token.uid.to_raw(),
            expires_in=token.expires_in.to_raw(),
            token_id=token_id.to_raw(),
        )
