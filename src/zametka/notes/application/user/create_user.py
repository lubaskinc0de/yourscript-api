from dataclasses import dataclass

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.common.interactor import Interactor
from zametka.notes.application.common.repository import UserRepository
from zametka.notes.application.common.uow import UoW
from zametka.notes.application.user.dto import UserDTO
from zametka.notes.domain.entities.user import User

from zametka.notes.domain.value_objects.user.user_first_name import (
    UserFirstName,
)
from zametka.notes.domain.value_objects.user.user_last_name import UserLastName


@dataclass(frozen=True)
class CreateUserInputDTO:
    first_name: str
    last_name: str


class CreateUser(Interactor[CreateUserInputDTO, UserDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.uow = uow
        self.id_provider = id_provider
        self.user_repository = user_repository

    async def __call__(self, data: CreateUserInputDTO) -> UserDTO:
        first_name = UserFirstName(data.first_name)
        last_name = UserLastName(data.last_name)
        user_id = await self.id_provider.get_user_id()

        user = User(
            first_name=first_name, last_name=last_name, user_id=user_id
        )

        user_dto = await self.user_repository.create(user)

        await self.uow.commit()

        return user_dto
