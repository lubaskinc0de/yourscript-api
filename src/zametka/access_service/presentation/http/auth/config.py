from dataclasses import dataclass


@dataclass
class TokenAuthConfig:
    token_cookie_key: str
    csrf_cookie_key: str
    csrf_headers_key: str
