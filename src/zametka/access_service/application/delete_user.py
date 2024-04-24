from dataclasses import dataclass

from zametka.access_service.application.common.event import EventEmitter
from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import (
    UserGateway,
)
from zametka.access_service.application.dto import UserDeletedEvent

from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class DeleteUserInputDTO:
    password: str


class DeleteUser(Interactor[DeleteUserInputDTO, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        user_provider: UserProvider,
        event_emitter: EventEmitter[UserDeletedEvent],
    ):
        self.user_gateway = user_gateway
        self.user_provider = user_provider
        self.event_emitter = event_emitter

    async def __call__(self, data: DeleteUserInputDTO) -> None:
        user = await self.user_provider.get_user()
        raw_password = UserRawPassword(data.password)

        user.ensure_can_access()
        user.ensure_passwords_match(raw_password)

        await self.user_gateway.delete(user.user_id)

        event = UserDeletedEvent(
            user_id=user.user_id.to_raw(),
        )
        await self.event_emitter.emit(event)

        return None
