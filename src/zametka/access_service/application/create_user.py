import logging
from dataclasses import dataclass
from uuid import uuid4

from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class CreateUserInputDTO:
    email: str
    password: str


class CreateUser(Interactor[CreateUserInputDTO, UserDTO]):
    def __init__(
        self,
        user_gateway: UserGateway,
        token_sender: TokenSender,
        uow: UoW,
    ):
        self.uow = uow
        self.token_sender = token_sender
        self.user_gateway = user_gateway

    async def __call__(self, data: CreateUserInputDTO) -> UserDTO:
        email = UserEmail(data.email)
        raw_password = UserRawPassword(data.password)
        user_id = UserId(value=uuid4())

        user = User.create_with_raw_password(
            user_id,
            email,
            raw_password,
        )

        user_dto = await self.user_gateway.create(user)
        await self.uow.commit()

        token: UserConfirmationToken = UserConfirmationToken(user.user_id)

        await self.token_sender.send(token, user)

        logging.info("Uid=%s created.", str(user_id.to_raw()))

        return user_dto
