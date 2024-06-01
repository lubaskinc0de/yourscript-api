from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.infrastructure.access_api_client import AccessAPIClient


class RawIdProvider(IdProvider):
    def __init__(self, user_id: UserId) -> None:
        self._user_id = user_id

    async def get_user_id(self) -> UserId:
        return self._user_id


class TokenIdProvider(IdProvider):
    def __init__(self, api_client: AccessAPIClient):
        self._api_client = api_client

    async def get_user_id(self) -> UserId:
        user_id = await self._api_client.get_identity()

        return user_id
