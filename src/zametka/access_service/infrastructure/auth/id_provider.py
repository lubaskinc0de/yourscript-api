from typing import Optional

from zametka.access_service.application.common.id_provider import (
    IdProvider,
)
from zametka.access_service.application.common.user_gateway import UserReader
from zametka.access_service.domain.common.services.access_service import AccessService
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.access_token import (
    UnauthorizedError,
)
from zametka.access_service.domain.exceptions.user import (
    UserIsNotExistsError,
)
from zametka.access_service.domain.value_objects.user_id import UserId


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: AccessToken,
        access_service: AccessService,
        user_gateway: UserReader,
    ):
        self._token = token
        self._user_id: Optional[UserId] = None
        self._user_gateway = user_gateway
        self._access_service = access_service

    def _get_id(self) -> UserId:
        if self._user_id:
            return self._user_id

        user_id = self._token.uid
        self._user_id = user_id

        return user_id

    async def get_user(self) -> User:
        user_id = self._get_id()
        user = await self._user_gateway.with_id(user_id)

        if not user:
            raise UnauthorizedError from UserIsNotExistsError

        self._access_service.authorize(user)

        return user
