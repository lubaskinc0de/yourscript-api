from uuid import uuid4

import pytest

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeUserProvider
from tests.mocks.access_service.user_identity_repository import (
    FakeUserGateway,
)
from zametka.access_service.application.delete_user import (
    DeleteUser,
    DeleteUserInputDTO,
)

from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
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


@pytest.fixture
def event_emitter() -> FakeEventEmitter:
    return FakeEventEmitter()

@pytest.mark.access
@pytest.mark.application
async def test_delete_identity(
    user_gateway: FakeUserGateway,
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_gateway.user.is_active = True

    interactor = DeleteUser(
        user_provider=user_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
    )

    result = await interactor(
        DeleteUserInputDTO(
            password=USER_PASSWORD,
        )
    )

    assert result is None
    assert user_provider.requested is True
    assert user_gateway.deleted is True
    assert event_emitter.calls(UserDeletedEvent)

@pytest.mark.access
@pytest.mark.application
async def test_delete_identity_not_active(
    user_gateway: FakeUserGateway,
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    interactor = DeleteUser(
        user_provider=user_provider,
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
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_gateway.user.is_active = True

    interactor = DeleteUser(
        user_provider=user_provider,
        event_emitter=event_emitter,
        user_gateway=user_gateway,
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(DeleteUserInputDTO(password=USER_PASSWORD + "fake"))
