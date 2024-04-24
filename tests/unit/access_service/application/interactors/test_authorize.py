from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserGateway,
)
from tests.mocks.access_service.token_sender import FakeTokenSender

from zametka.access_service.application.authorize import (
    Authorize,
    AuthorizeInputDTO,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    UserIsNotExistsError,
    InvalidCredentialsError,
)

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
    user = User.create_with_raw_password(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_PASSWORD),
        user_id=UserId(USER_ID),
    )
    user.is_active = True

    return FakeUserGateway(
        user,
    )


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


@pytest.mark.access
@pytest.mark.application
async def test_authorize(
        user_gateway: FakeUserGateway,
        token_sender: FakeTokenSender,
) -> None:
    interactor = Authorize(
        user_gateway,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserDTO) is True

    assert result.user_id == user_gateway.user.user_id.to_raw()


@pytest.mark.access
@pytest.mark.application
async def test_authorize_not_active(
        user_gateway: FakeUserGateway,
        token_sender: FakeTokenSender,
) -> None:
    user_gateway.user.is_active = False

    interactor = Authorize(
        user_gateway,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor(dto)


@pytest.mark.access
@pytest.mark.application
async def test_authorize_not_exists(
        user_gateway: FakeUserGateway,
        token_sender: FakeTokenSender,
) -> None:
    async def fake_get(*_):
        return None

    user_gateway.get_by_email = fake_get

    interactor = Authorize(
        user_gateway,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)


@pytest.mark.access
@pytest.mark.application
async def test_authorize_bad_password(
        user_gateway: FakeUserGateway,
        token_sender: FakeTokenSender,
) -> None:
    interactor = Authorize(
        user_gateway,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD + "FAKE",
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(dto)
