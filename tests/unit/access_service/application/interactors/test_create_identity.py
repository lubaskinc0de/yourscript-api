from datetime import timedelta

import pytest

from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.token_sender import FakeTokenSender
from tests.unit.access_service.application.interactors.const import USER_PASSWORD

from zametka.access_service.application.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.config import UserConfirmationTokenConfig


@pytest.mark.access
@pytest.mark.application
async def test_create_identity(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
    token_sender: FakeTokenSender,
) -> None:
    interactor = CreateUser(
        user_gateway=user_gateway,
        uow=uow,
        token_sender=token_sender,
        config=UserConfirmationTokenConfig(expires_after=timedelta(minutes=15)),
    )

    dto = CreateUserInputDTO(
        email=user_gateway.user.email.to_raw(),
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserDTO) is True

    assert uow.committed is True

    assert user_gateway.saved is True
    assert result.user_id == user_gateway.user.user_id

    assert token_sender.token_sent_cnt == 1
