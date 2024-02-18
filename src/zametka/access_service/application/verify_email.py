from dataclasses import dataclass
from datetime import datetime

from typing import Optional
from uuid import UUID

from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.domain.entities.user_identity import UserIdentity

from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.exceptions.user_identity import UserIsNotExistsError
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


@dataclass(frozen=True)
class TokenInputDTO:
    uid: UUID
    timestamp: datetime


class VerifyEmail(Interactor[TokenInputDTO, None]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        uow: UoW,
    ):
        self.uow = uow
        self.user_repository = user_repository

    async def __call__(self, data: TokenInputDTO) -> None:
        user: Optional[UserIdentity] = await self.user_repository.get(
            UserIdentityId(data.uid)
        )

        if not user:
            raise UserIsNotExistsError()

        token = IdentityConfirmationToken.load(user.identity_id, data.timestamp)
        user.activate(token)

        await self.user_repository.update(user.identity_id, user)
        await self.uow.commit()

        return None
