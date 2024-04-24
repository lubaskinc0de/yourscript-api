from datetime import datetime, timezone
from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserGateway,
)
from tests.mocks.access_service.uow import FakeUoW

from zametka.access_service.application.verify_email import VerifyEmail, TokenInputDTO
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import UserIsNotExistsError

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


@pytest.mark.skip(reason="Helper function")
def get_token_with_incorrect_uid() -> UserConfirmationToken:
    return UserConfirmationToken(uid=UserId(uuid4()))

@pytest.mark.access
@pytest.mark.application
async def test_verify_email(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
) -> None:
    assert user_gateway.user.is_active is False

    interactor = VerifyEmail(
        user_gateway,
        uow=uow,
    )

    token = UserConfirmationToken(uid=user_gateway.user.user_id)

    dto = TokenInputDTO(
        uid=token.uid.to_raw(),
        timestamp=datetime.now(tz=timezone.utc),
    )

    result = await interactor(dto)

    assert result is None
    assert uow.committed is True
    assert user_gateway.user.is_active is True

@pytest.mark.access
@pytest.mark.application
async def test_verify_incorrect_email(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
) -> None:
    assert user_gateway.user.is_active is False

    interactor = VerifyEmail(
        user_gateway=user_gateway,
        uow=uow,
    )

    token = get_token_with_incorrect_uid()

    dto = TokenInputDTO(
        uid=token.uid.to_raw(),
        timestamp=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)
