import pytest

from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.token_sender import FakeTokenSender

from zametka.access_service.application.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.config import (
    UserConfirmationTokenConfig,
)
from zametka.access_service.domain.services.password_hasher import (
    PasswordHasher,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@pytest.mark.access
@pytest.mark.application
async def test_create_identity(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
    token_sender: FakeTokenSender,
    password_hasher: PasswordHasher,
    confirmation_token_config: UserConfirmationTokenConfig,
    user_password: UserRawPassword,
    user_email: UserEmail,
) -> None:
    interactor = CreateUser(
        user_gateway=user_gateway,
        uow=uow,
        token_sender=token_sender,
        config=confirmation_token_config,
        password_hasher=password_hasher,
    )

    dto = CreateUserInputDTO(
        email=user_email.to_raw(),
        password=user_password.to_raw(),
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserDTO) is True

    assert uow.committed is True

    assert user_gateway.saved is True
    assert result.user_id == user_gateway.user.user_id

    assert token_sender.token_sent_cnt == 1
