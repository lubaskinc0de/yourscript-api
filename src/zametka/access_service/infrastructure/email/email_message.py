from dataclasses import dataclass


@dataclass
class EmailMessage:
    email_from: str
    email_to: str
    subject: str
    content: str
