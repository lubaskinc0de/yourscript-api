from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserGateway,
)
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.token_sender import FakeTokenSender

from zametka.access_service.application.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

USER_EMAIL = "lubaskincorporation@gmail.com"
USER_PASSWORD = "someSuper123#Password"
USER_ID = uuid4()


@pytest.fixture
def user_gateway() -> FakeUserGateway:
    return FakeUserGateway(
        User.create_with_raw_password(
            email=UserEmail(USER_EMAIL),
            raw_password=UserRawPassword(USER_PASSWORD),
            user_id=UserId(USER_ID),
        )
    )


@pytest.fixture
def uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


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
    )

    dto = CreateUserInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserDTO) is True

    assert uow.committed is True

    assert user_gateway.created is True
    assert result.user_id == USER_ID

    assert token_sender.token_sent_cnt == 1
