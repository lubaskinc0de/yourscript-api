import pytest

from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)

from zametka.access_service.application.get_user import (
    GetUser,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.exceptions.user import UserIsNotActiveError


@pytest.mark.access
@pytest.mark.application
@pytest.mark.parametrize(
    ["user_is_active", "exc_class"],
    [
        (True, None),
        (False, UserIsNotActiveError),
    ],
)
async def test_get_identity(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
    user_is_active: bool,
    exc_class,
) -> None:
    user_gateway.user.is_active = user_is_active

    interactor = GetUser(
        id_provider=id_provider,
    )

    coro = interactor()

    if not exc_class:
        result = await coro
        assert result is not None
        assert isinstance(result, UserDTO) is True
        assert result.user_id == id_provider.user.user_id
        assert id_provider.requested is True
    else:
        with pytest.raises(exc_class):
            await coro
