from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.common.interactor import Interactor
from zametka.notes.application.common.repository import UserRepository
from zametka.notes.application.user.dto import UserDTO
from zametka.notes.domain.exceptions.user import UserIsNotExistsError


class GetUser(Interactor[None, UserDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        id_provider: IdProvider,
    ):
        self.user_repository = user_repository
        self.id_provider = id_provider

    async def __call__(self, data=None) -> UserDTO:  # type:ignore
        user_id = await self.id_provider.get_user_id()
        user = await self.user_repository.get(user_id=user_id)

        if not user:
            raise UserIsNotExistsError()

        return UserDTO(
            first_name=user.first_name,
            last_name=user.last_name,
            joined_at=user.joined_at,
        )
