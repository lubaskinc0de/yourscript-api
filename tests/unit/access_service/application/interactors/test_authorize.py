import pytest

from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)
from tests.mocks.access_service.token_sender import FakeTokenSender
from tests.unit.access_service.application.interactors.const import USER_PASSWORD

from zametka.access_service.application.authorize import (
    Authorize,
    AuthorizeInputDTO,
)
from zametka.access_service.application.dto import AccessTokenDTO
from zametka.access_service.domain.entities.config import AccessTokenConfig

from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    UserIsNotExistsError,
    InvalidCredentialsError,
)


@pytest.mark.access
@pytest.mark.application
async def test_authorize(
    user_gateway: FakeUserGateway,
    access_token_config: AccessTokenConfig,
) -> None:
    user_gateway.user.is_active = True

    interactor = Authorize(
        user_gateway,
        access_token_config,
    )

    dto = AuthorizeInputDTO(
        email=user_gateway.user.email.to_raw(),
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, AccessTokenDTO) is True

    assert result.uid == user_gateway.user.user_id.to_raw()


@pytest.mark.access
@pytest.mark.application
async def test_authorize_not_active(
    user_gateway: FakeUserGateway,
    token_sender: FakeTokenSender,
    access_token_config: AccessTokenConfig,
) -> None:
    user_gateway.user.is_active = False

    interactor = Authorize(
        user_gateway,
        access_token_config,
    )

    dto = AuthorizeInputDTO(
        email=user_gateway.user.email.to_raw(),
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor(dto)


@pytest.mark.access
@pytest.mark.application
async def test_authorize_not_exists(
    user_gateway: FakeUserGateway,
    token_sender: FakeTokenSender,
    access_token_config: AccessTokenConfig,
) -> None:
    async def fake_get(*_):
        return None

    user_gateway.get_by_email = fake_get

    interactor = Authorize(
        user_gateway,
        access_token_config,
    )

    dto = AuthorizeInputDTO(
        email=user_gateway.user.email.to_raw(),
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)


@pytest.mark.access
@pytest.mark.application
async def test_authorize_bad_password(
    user_gateway: FakeUserGateway,
    token_sender: FakeTokenSender,
    access_token_config: AccessTokenConfig,
) -> None:
    interactor = Authorize(
        user_gateway,
        access_token_config,
    )

    dto = AuthorizeInputDTO(
        email=user_gateway.user.email.to_raw(),
        password=USER_PASSWORD + "FAKE",
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(dto)
