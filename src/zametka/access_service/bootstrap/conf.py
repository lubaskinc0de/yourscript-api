import logging
import os
import tomllib
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

from zametka.access_service.domain.entities.config import (
    AccessTokenConfig,
    UserConfirmationTokenConfig,
)
from zametka.access_service.infrastructure.email.config import (
    ConfirmationEmailConfig,
    SMTPConfig,
)
from zametka.access_service.infrastructure.jwt.config import JWTConfig
from zametka.access_service.infrastructure.message_broker.config import (
    AMQPConfig,
)
from zametka.access_service.infrastructure.persistence.config import DBConfig
from zametka.access_service.presentation.http.auth.config import TokenAuthConfig


def load_config_by_path(config_path: Path) -> dict[str, Any]:
    with config_path.open("rb") as cfg:
        return tomllib.load(cfg)


@dataclass
class AllConfig:
    db: DBConfig
    amqp: AMQPConfig
    smtp: SMTPConfig
    email: ConfirmationEmailConfig
    jwt: JWTConfig
    token_auth: TokenAuthConfig
    access_token: AccessTokenConfig
    confirmation_token: UserConfirmationTokenConfig


def load_all_config() -> AllConfig:
    db = DBConfig(
        db_name=os.environ["ACCESS_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )

    amqp = AMQPConfig(
        host=os.environ.get("AMQP_HOST", "localhost"),
        port=int(os.environ.get("AMQP_PORT", 5672)),
        login=os.environ.get("AMQP_LOGIN", "guest"),
        password=os.environ.get("AMQP_PASSWORD", "guest"),
    )

    cfg_path = os.environ["CONFIG_PATH"]
    cfg = load_config_by_path(Path(cfg_path))

    try:
        email_subject = cfg["email"]["activation-mail-subject"]
        email_url = cfg["email"]["activation-url-template"]
        email_template_path = cfg["email"]["activation-email-template-path"]
        email_template_name = cfg["email"]["activation-email-template-name"]

        smtp_use_tls = cfg["smtp"]["use-tls"]
        smtp_host = cfg["smtp"]["host"]
        smtp_port = cfg["smtp"]["port"]

        jwt_algorithm = cfg["security"]["algorithm"]
        jwt_token_key = cfg["auth"]["auth-token-key"]

        access_token_expires_after = cfg["security"]["access-token-expires-minutes"]
        confirmation_token_expires_after = cfg["security"][
            "confirmation-token-expires-minutes"
        ]
    except KeyError:
        logging.fatal("On startup: Error reading config %s", cfg_path)
        raise

    email = ConfirmationEmailConfig(
        email_from=os.environ["MAIL_FROM"],
        subject=email_subject,
        confirmation_link=email_url,
        template_path=email_template_path,
        template_name=email_template_name,
    )

    smtp = SMTPConfig(
        password=os.environ["MAIL_PASSWORD"],
        user=os.environ["MAIL_USERNAME"],
        host=smtp_host,
        port=smtp_port,
        use_tls=smtp_use_tls,
    )

    jwt = JWTConfig(algorithm=jwt_algorithm, key=os.environ["JWT_KEY"])

    token_auth = TokenAuthConfig(token_key=jwt_token_key)

    access_token = AccessTokenConfig(
        expires_after=timedelta(minutes=access_token_expires_after),
    )

    confirmation_token = UserConfirmationTokenConfig(
        expires_after=timedelta(minutes=confirmation_token_expires_after),
    )

    logging.info("Config loaded.")

    return AllConfig(
        db=db,
        amqp=amqp,
        smtp=smtp,
        email=email,
        jwt=jwt,
        token_auth=token_auth,
        access_token=access_token,
        confirmation_token=confirmation_token,
    )
