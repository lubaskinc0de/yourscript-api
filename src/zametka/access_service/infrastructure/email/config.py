from dataclasses import dataclass


@dataclass
class SMTPConfig:
    user: str
    password: str
    port: int
    host: str
    use_tls: bool


@dataclass
class ConfirmationEmailConfig:
    subject: str
    confirmation_link: str
    email_from: str
    template_path: str
    template_name: str
