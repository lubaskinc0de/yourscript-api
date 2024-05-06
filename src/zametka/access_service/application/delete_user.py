from dataclasses import dataclass

from zametka.access_service.application.common.event import EventEmitter
from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.user_gateway import (
    UserSaver,
)
from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.domain.services.password_hasher import (
    PasswordHasher,
)

from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class DeleteUserInputDTO:
    password: str


class DeleteUser(Interactor[DeleteUserInputDTO, None]):
    def __init__(
        self,
        user_gateway: UserSaver,
        id_provider: IdProvider,
        event_emitter: EventEmitter[UserDeletedEvent],
        password_hasher: PasswordHasher,
    ):
        self.user_gateway = user_gateway
        self.id_provider = id_provider
        self.event_emitter = event_emitter
        self.ph = password_hasher

    async def __call__(self, data: DeleteUserInputDTO) -> None:
        user = await self.id_provider.get_user()
        raw_password = UserRawPassword(data.password)

        user.authenticate(raw_password, self.ph)
        await self.user_gateway.delete(user.user_id)

        event = UserDeletedEvent(
            user_id=user.user_id.to_raw(),
        )
        await self.event_emitter.emit(event)

        return None
