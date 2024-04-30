from typing import Optional

from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.domain.entities.user import User

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.user_identity import UserIsNotExistsError


class VerifyEmail(Interactor[UserConfirmationToken, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        uow: UoW,
    ):
        self.uow = uow
        self.user_gateway = user_gateway

    async def __call__(self, data: UserConfirmationToken) -> None:
        user: Optional[User] = await self.user_gateway.get(data.uid)

        if not user:
            raise UserIsNotExistsError()

        user.activate(data)

        await self.user_gateway.update(user.user_id, user)
        await self.uow.commit()

        return None
