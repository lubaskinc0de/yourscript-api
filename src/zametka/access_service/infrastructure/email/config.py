from dataclasses import dataclass


@dataclass
class SMTPConfig:
    user: str
    password: str
    port: int
    host: str
    use_tls: bool


@dataclass
class ActivationEmailConfig:
    subject: str
    activation_url: str
    email_from: str
    template_path: str
    template_name: str
