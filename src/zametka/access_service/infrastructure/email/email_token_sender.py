import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment

from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.entities.user import User
from zametka.access_service.infrastructure.email.config import ActivationEmailConfig
from zametka.access_service.infrastructure.email.email_client import EmailClient
from zametka.access_service.infrastructure.jwt.confirmation_token_processor import (
    ConfirmationTokenProcessor,
)


class EmailTokenSender(TokenSender):
    def __init__(
        self,
        client: EmailClient,
        jinja: Environment,
        config: ActivationEmailConfig,
        token_processor: ConfirmationTokenProcessor,
    ) -> None:
        self.client = client
        self.jinja = jinja
        self.config = config
        self.token_processor = token_processor

    def _render_html(self, token: UserConfirmationToken) -> str:
        template = self.jinja.get_template(self.config.template_name)
        jwt_token = self.token_processor.encode(token)

        logging.info(jwt_token)
        rendered: str = template.render(
            token_link=self.config.activation_url.format(jwt_token)
        )

        return rendered

    async def send(self, token: UserConfirmationToken, user: User) -> None:
        html = self._render_html(token)
        message = MIMEMultipart("alternative")

        message["From"] = self.config.email_from
        message["To"] = user.email.to_raw()
        message["Subject"] = self.config.subject

        html_text = MIMEText(html, "html")
        message.attach(html_text)

        await self.client.send(message)

        logging.info("Email sent to uid=%s", str(user.user_id.to_raw()))
