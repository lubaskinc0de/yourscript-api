from typing import Optional

from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.domain.common.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.entities.user import User

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.user import UserIsNotExistsError
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId


class VerifyEmail(Interactor[UserConfirmationTokenDTO, None]):
    def __init__(
        self,
        user_reader: UserReader,
        user_saver: UserSaver,
        uow: UoW,
    ):
        self.uow = uow
        self.user_reader = user_reader
        self.user_saver = user_saver

    async def __call__(self, data: UserConfirmationTokenDTO) -> None:
        metadata = TimedTokenMetadata(
            uid=UserId(data.uid), expires_in=ExpiresIn(data.expires_in)
        )
        token = UserConfirmationToken(metadata)

        user: Optional[User] = await self.user_reader.with_id(token.uid)

        if not user:
            raise UserIsNotExistsError

        user.activate(token)

        await self.user_saver.save(user)
        await self.uow.commit()

        return None
