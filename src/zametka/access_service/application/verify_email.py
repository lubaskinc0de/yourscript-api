from dataclasses import dataclass
from datetime import datetime

from typing import Optional
from uuid import UUID

from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.domain.entities.user import User

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.user_identity import UserIsNotExistsError
from zametka.access_service.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class TokenInputDTO:
    uid: UUID
    timestamp: datetime


class VerifyEmail(Interactor[TokenInputDTO, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        uow: UoW,
    ):
        self.uow = uow
        self.user_gateway = user_gateway

    async def __call__(self, data: TokenInputDTO) -> None:
        user: Optional[User] = await self.user_gateway.get(
            UserId(data.uid)
        )

        if not user:
            raise UserIsNotExistsError()

        token = UserConfirmationToken.load(user.user_id, data.timestamp)
        user.activate(token)

        await self.user_gateway.update(user.user_id, user)
        await self.uow.commit()

        return None
