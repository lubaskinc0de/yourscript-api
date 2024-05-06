import pytest

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeIdProvider
from tests.mocks.access_service.token_sender import FakeTokenSender
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.user_gateway import FakeUserGateway


from zametka.access_service.domain.entities.user import User


@pytest.fixture
def user_gateway(user: User) -> FakeUserGateway:
    return FakeUserGateway(user)


@pytest.fixture
def id_provider(
    user: User,
) -> FakeIdProvider:
    return FakeIdProvider(user)


@pytest.fixture
def uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


@pytest.fixture
def event_emitter() -> FakeEventEmitter:
    return FakeEventEmitter()
