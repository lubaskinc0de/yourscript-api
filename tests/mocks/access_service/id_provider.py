from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.domain.entities.user import User


class FakeIdProvider(IdProvider):
    def __init__(self, user: User):
        self.requested = False
        self.user = user

    async def get_user(self) -> User:
        self.user.ensure_is_active()
        self.requested = True
        return self.user
