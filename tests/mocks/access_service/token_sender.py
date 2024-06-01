from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.domain.entities.user import User


class FakeTokenSender(TokenSender):
    def __init__(self):
        self.token_sent_cnt = 0

    async def send(
        self,
        confirmation_token: UserConfirmationTokenDTO,
        user: User,
    ) -> None:
        self.token_sent_cnt += 1
