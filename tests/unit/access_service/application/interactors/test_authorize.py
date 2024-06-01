import pytest
from zametka.access_service.application.authorize import (
    Authorize,
    AuthorizeInputDTO,
)
from zametka.access_service.application.common.exceptions.user import (
    UserIsNotExistsError,
)
from zametka.access_service.application.dto import AccessTokenDTO
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotActiveError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)


@pytest.mark.access
@pytest.mark.application
@pytest.mark.parametrize(
    ["user_is_active", "user_is_exists", "password_startswith", "exc_class"],
    [
        (True, True, "", None),
        (False, True, "", UserIsNotActiveError),
        (True, False, "", UserIsNotExistsError),
        (True, True, "blabla", InvalidCredentialsError),
    ],
)
async def test_authorize(
    user_gateway: FakeUserGateway,
    access_token_config: AccessTokenConfig,
    user_password: UserRawPassword,
    user_email: UserEmail,
    password_hasher: PasswordHasher,
    user_is_active: bool,
    user_is_exists: bool,
    password_startswith: str,
    exc_class,
) -> None:
    user_gateway.user.is_active = user_is_active

    if not user_is_exists:

        async def fake_get(*_):
            return None

        user_gateway.with_email = fake_get

    interactor = Authorize(
        user_gateway,
        access_token_config,
        password_hasher,
    )

    dto = AuthorizeInputDTO(
        email=user_email.to_raw(),
        password=password_startswith + user_password.to_raw(),
    )

    coro = interactor(dto)

    if exc_class:
        with pytest.raises(exc_class):
            await coro
    else:
        result = await coro

        assert result is not None
        assert isinstance(result, AccessTokenDTO) is True

        assert result.uid == user_gateway.user.user_id.to_raw()
