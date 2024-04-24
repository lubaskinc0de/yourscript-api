import logging

from jinja2 import Environment

from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.infrastructure.email.email_client import EmailClient
# from zametka.access_service.infrastructure.email.email_message import EmailMessage


class EmailTokenSender(TokenSender):
    def __init__(
        self,
        client: EmailClient,
        jinja: Environment,  # TODO: pass config here
    ) -> None:
        self._client = client
        self._jinja = jinja

    def _render_html(self, confirmation_token: UserConfirmationToken) -> str:
        template = self._jinja.get_template("confirmation-email.html")

        rendered: str = template.render(
            token_link="#"  # TODO:
        )

        return rendered

    async def send(self, token: UserConfirmationToken, user: User) -> None:
        """Send email token to the user"""

        html = self._render_html(token)
        # message = EmailMessage(
        #     subject="ЗАВЕРШИТЕ РЕГИСТРАЦИЮ В zametka.",  # TODO: take it from config
        #     content=html,
        #     email_to=user.email,
        #     email_from=# TODO: TAKE IT FROM CONFIG
        # )

        # await self._client.send(...) # TODO: ...

        logging.info("email sent")
