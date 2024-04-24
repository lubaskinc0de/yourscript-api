from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_id import UserId


class FakeUserProvider(UserProvider):
    def __init__(self, user: User):
        self.requested = False
        self.user = user

    def get_user_id(self) -> UserId:
        if self.requested:
            raise ValueError("Identity requested twice! Please, check your interactor.")

        self.requested = True
        return self.user.user_id

    async def get_user(self) -> User:
        if self.requested:
            raise ValueError("Identity requested twice! Please, check your interactor.")

        self.requested = True
        return self.user
