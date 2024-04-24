from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.application.common.interactor import Interactor


class GetUser(Interactor[None, UserDTO]):
    def __init__(
        self,
        user_provider: UserProvider,
    ):
        self.user_provider = user_provider

    async def __call__(self, data=None) -> UserDTO:  # type:ignore
        user = await self.user_provider.get_user()
        user.ensure_can_access()

        return UserDTO(
            user_id=user.user_id.to_raw(),
        )
