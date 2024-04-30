from zametka.access_service.application.common.id_provider import (
    UserProvider,
    IdProvider,
)
from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import (
    IsNotAuthorizedError,
    UserIsNotExistsError,
)
from zametka.access_service.domain.value_objects.user_id import UserId


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: AccessToken,
    ):
        self._token = token
        self._user_id = None

    def _get_id(self) -> UserId:
        if self._user_id:
            return self._user_id

        user_id = self._token.uid
        self._user_id = user_id

        return user_id

    def get_user_id(self) -> UserId:
        return self._get_id()


class UserProviderImpl(UserProvider):
    def __init__(self, id_provider: IdProvider, user_gateway: UserGateway) -> None:
        self._id_provider = id_provider
        self.user_gateway = user_gateway

    def get_user_id(self) -> UserId:
        return self._id_provider.get_user_id()

    async def get_user(self) -> User:
        user_id = self.get_user_id()
        user = await self.user_gateway.get(user_id)

        if not user:
            raise IsNotAuthorizedError() from UserIsNotExistsError()

        return user
