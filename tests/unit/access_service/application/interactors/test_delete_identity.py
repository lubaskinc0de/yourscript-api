import pytest

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)
from tests.unit.access_service.application.interactors.const import USER_PASSWORD
from zametka.access_service.application.delete_user import (
    DeleteUser,
    DeleteUserInputDTO,
)

from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.domain.exceptions.user import (
    UserIsNotActiveError,
    InvalidCredentialsError,
)


@pytest.mark.access
@pytest.mark.application
async def test_delete_identity(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_gateway.user.is_active = True

    interactor = DeleteUser(
        id_provider=id_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
    )

    result = await interactor(
        DeleteUserInputDTO(
            password=USER_PASSWORD,
        )
    )

    assert result is None
    assert id_provider.requested is True
    assert user_gateway.deleted is True
    assert event_emitter.calls(UserDeletedEvent)


@pytest.mark.access
@pytest.mark.application
async def test_delete_identity_not_active(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    interactor = DeleteUser(
        id_provider=id_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor(
            DeleteUserInputDTO(
                password=USER_PASSWORD,
            )
        )


@pytest.mark.access
@pytest.mark.application
async def test_delete_identity_bad_password(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_gateway.user.is_active = True

    interactor = DeleteUser(
        id_provider=id_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(DeleteUserInputDTO(password=USER_PASSWORD + "fake"))
