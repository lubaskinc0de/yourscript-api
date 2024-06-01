import pytest
from zametka.access_service.application.delete_user import (
    DeleteUser,
    DeleteUserInputDTO,
)
from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotActiveError,
)
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)


@pytest.mark.access
@pytest.mark.application
@pytest.mark.parametrize(
    ["user_is_active", "password_startswith", "exc_class"],
    [
        (True, "", None),
        (False, "", UserIsNotActiveError),
        (True, "blabla", InvalidCredentialsError),
    ],
)
async def test_delete_identity(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
    event_emitter: FakeEventEmitter,
    password_hasher: PasswordHasher,
    user_password: UserRawPassword,
    user_is_active: bool,
    password_startswith: str,
    exc_class,
) -> None:
    user_gateway.user.is_active = user_is_active

    interactor = DeleteUser(
        id_provider=id_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
        password_hasher=password_hasher,
    )

    coro = interactor(
        DeleteUserInputDTO(
            password=password_startswith + user_password.to_raw(),
        ),
    )

    if exc_class:
        with pytest.raises(exc_class):
            await coro
    else:
        result = await coro

        assert result is None
        assert id_provider.requested is True
        assert user_gateway.deleted is True
        assert event_emitter.calls(UserDeletedEvent)
