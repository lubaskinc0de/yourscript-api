from dataclasses import dataclass


@dataclass
class MailConfig:
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
