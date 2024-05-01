from datetime import timedelta

import pytest

from zametka.access_service.domain.entities.config import UserConfirmationTokenConfig


@pytest.fixture
def confirmation_token_config() -> UserConfirmationTokenConfig:
    return UserConfirmationTokenConfig(
        expires_after=timedelta(minutes=15),
    )
