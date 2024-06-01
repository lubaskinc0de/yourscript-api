import pytest
from zametka.access_service.application.common.exceptions.user import (
    UserIsNotExistsError,
)
from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)

from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.user_gateway import (
    FakeUserGateway,
)


@pytest.mark.access
@pytest.mark.application
@pytest.mark.parametrize(
    ["token_fixture_name", "exc_class"],
    [
        ("confirmation_token", None),
        ("fake_confirmation_token", UserIsNotExistsError),
        ("expired_confirmation_token", ConfirmationTokenIsExpiredError),
    ],
)
async def test_verify_email(
    user_gateway: FakeUserGateway,
    uow: FakeUoW,
    token_fixture_name: str,
    exc_class,
    request,
) -> None:
    interactor = VerifyEmail(
        uow=uow,
        user_reader=user_gateway,
        user_saver=user_gateway,
    )

    token: UserConfirmationToken = request.getfixturevalue(token_fixture_name)

    dto = UserConfirmationTokenDTO(
        uid=token.uid.to_raw(),
        expires_in=token.expires_in.to_raw(),
        token_id=token.token_id.to_raw(),
    )

    coro = interactor(dto)

    if not exc_class:
        result = await coro

        assert result is None
        assert uow.committed is True
        assert user_gateway.user.is_active is True
    else:
        with pytest.raises(exc_class):
            await coro
