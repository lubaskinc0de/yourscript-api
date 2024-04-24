import logging
import os

from dataclasses import dataclass

from zametka.access_service.infrastructure.email.config import MailConfig
from zametka.access_service.infrastructure.message_broker.config import AMQPConfig
from zametka.access_service.infrastructure.persistence.config import DBConfig


@dataclass
class AllConfig:
    db: DBConfig
    amqp: AMQPConfig
    mail: MailConfig


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

    mail = MailConfig(
        mail_from=os.environ["MAIL_FROM"],
        mail_from_name=os.environ["MAIL_FROM_NAME"],
        mail_password=os.environ["MAIL_PASSWORD"],
        mail_port=int(os.environ.get("MAIL_PORT", 443)),
        mail_server=os.environ["MAIL_SERVER"],
        mail_username=os.environ["MAIL_USERNAME"],
    )

    logging.info("Access config was loaded.")

    return AllConfig(
        db=db,
        amqp=amqp,
        mail=mail,
    )
