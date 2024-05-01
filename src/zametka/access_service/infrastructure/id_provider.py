from zametka.access_service.application.common.id_provider import (
    IdProvider,
)
from zametka.access_service.application.common.user_gateway import UserReader
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotExistsError,
)
from zametka.access_service.domain.value_objects.user_id import UserId


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: AccessToken,
        user_gateway: UserReader
    ):
        self._token = token
        self._user_id = None
        self._user_gateway = user_gateway

    def _get_id(self) -> UserId:
        if self._user_id:
            return self._user_id

        user_id = self._token.uid
        self._user_id = user_id

        return user_id

    async def get_user(self) -> User:
        user_id = self._get_id()
        user = await self._user_gateway.get(user_id)

        if not user:
            raise UnauthorizedError from UserIsNotExistsError

        user.ensure_authorized(self._token)

        return user
