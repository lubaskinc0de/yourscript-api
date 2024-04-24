import os
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class CORSConfig:
    frontend_url: str


@dataclass
class AuthJWTConfig:
    authjwt_secret_key: str

    authjwt_token_location: set[str]

    authjwt_access_token_expires: timedelta
    authjwt_cookie_expires: int

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True

    authjwt_cookie_samesite: str = 'lax'


def load_authjwt_config() -> AuthJWTConfig:
    return AuthJWTConfig(
        authjwt_secret_key=os.environ["AUTHJWT_SECRET_KEY"],
        authjwt_token_location={"cookies"},
        authjwt_access_token_expires=timedelta(
            minutes=int(os.environ["AUTHJWT_TOKEN_EXPIRES_MINUTES"])
        ),
        authjwt_cookie_expires=int(os.environ["AUTHJWT_COOKIE_EXPIRES_SECONDS"]),
    )