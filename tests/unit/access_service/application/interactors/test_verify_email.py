from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pytest

from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)
from tests.mocks.access_service.uow import FakeUoW
from zametka.access_service.application.dto import UserConfirmationTokenDTO

from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.domain.entities.config import UserConfirmationTokenConfig
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


@pytest.mark.access
@pytest.mark.application
async def test_verify_email(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
    confirmation_token_config: UserConfirmationTokenConfig,
) -> None:
    assert user_gateway.user.is_active is False

    interactor = VerifyEmail(
        user_gateway,
        uow=uow,
        config=confirmation_token_config,
    )

    token = UserConfirmationToken(uid=user_gateway.user.user_id, config=confirmation_token_config)

    dto = UserConfirmationTokenDTO(
        uid=token.uid.to_raw(),
        expires_in=datetime.now(tz=timezone.utc) + timedelta(minutes=5),
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
    confirmation_token_config: UserConfirmationTokenConfig,
    incorrect_confirmation_token: UserConfirmationToken,
) -> None:
    assert user_gateway.user.is_active is False

    interactor = VerifyEmail(
        user_gateway=user_gateway,
        uow=uow,
        config=confirmation_token_config,
    )

    token = incorrect_confirmation_token

    dto = UserConfirmationTokenDTO(
        uid=token.uid.to_raw(),
        expires_in=datetime.now(tz=timezone.utc) + timedelta(minutes=5),
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)
