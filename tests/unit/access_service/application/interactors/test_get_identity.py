from uuid import uuid4

import pytest

from tests.mocks.access_service.id_provider import FakeUserProvider
from tests.mocks.access_service.user_identity_repository import (
    FakeUserGateway,
)

from zametka.access_service.application.get_user import (
    GetUser,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import UserIsNotActiveError

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
def user_provider(
        user_gateway: FakeUserGateway,
) -> FakeUserProvider:
    return FakeUserProvider(user_gateway.user)


@pytest.mark.access
@pytest.mark.application
async def test_get_identity(
        user_gateway: FakeUserGateway,
        user_provider: FakeUserProvider,
) -> None:
    user_gateway.user.is_active = True

    interactor = GetUser(
        user_provider=user_provider,
    )

    result = await interactor()

    assert result is not None
    assert isinstance(result, UserDTO) is True
    assert result.user_id == USER_ID
    assert user_provider.requested is True


@pytest.mark.access
@pytest.mark.application
async def test_get_identity_not_active(
        user_provider: FakeUserProvider,
) -> None:
    interactor = GetUser(
        user_provider=user_provider,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor()
