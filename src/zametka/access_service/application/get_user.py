from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.dto import UserDTO


class GetUser(Interactor[None, UserDTO]):
    def __init__(
        self,
        id_provider: IdProvider,
    ):
        self.id_provider = id_provider

    async def __call__(self, data=None) -> UserDTO:
        user = await self.id_provider.get_user()
        return UserDTO(
            user_id=user.user_id.to_raw(),
        )
