import pytest

from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)

from zametka.access_service.application.get_user import (
    GetUser,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.exceptions.user_identity import UserIsNotActiveError


@pytest.mark.access
@pytest.mark.application
async def test_get_identity(
    user_gateway: FakeUserGateway,
    id_provider: FakeIdProvider,
) -> None:
    user_gateway.user.is_active = True

    interactor = GetUser(
        id_provider=id_provider,
    )

    result = await interactor()

    assert result is not None
    assert isinstance(result, UserDTO) is True
    assert result.user_id == id_provider.user.user_id
    assert id_provider.requested is True


@pytest.mark.access
@pytest.mark.application
async def test_get_identity_not_active(
    id_provider: FakeIdProvider,
) -> None:
    interactor = GetUser(
        id_provider=id_provider,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor()
