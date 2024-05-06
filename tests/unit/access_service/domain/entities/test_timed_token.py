import pytest

from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)


@pytest.mark.access
@pytest.mark.domain
@pytest.mark.parametrize(
    ["fixture_name", "exc_class"],
    [
        ("confirmation_token", None),
        ("expired_confirmation_token", ConfirmationTokenIsExpiredError),
    ],
)
def test_verify_token(fixture_name, exc_class, request):
    token = request.getfixturevalue(fixture_name)
    if not exc_class:
        token.verify()
    else:
        with pytest.raises(exc_class):
            token.verify()
