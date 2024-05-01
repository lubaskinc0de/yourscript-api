from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.common.interactor import Interactor


class GetUser(Interactor[None, UserDTO]):
    def __init__(
        self,
        id_provider: IdProvider,
    ):
        self.id_provider = id_provider

    async def __call__(self, data=None) -> UserDTO:  # type:ignore
        user = await self.id_provider.get_user()
        return UserDTO(
            user_id=user.user_id.to_raw(),
        )
