from email_validator import EmailNotValidError, validate_email

from pydantic import BaseModel, root_validator, validator

from zametka.access_service.domain.exceptions.user_identity import InvalidUserEmailError


def email_validator(email: str) -> str:
    try:
        email_info = validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise InvalidUserEmailError("Неправильный e-email!")

    email = email_info.original_email

    return email


class CreateIdentitySchema(BaseModel):
    email: str
    password: str
    password2: str

    @validator("email")
    def validate_email(cls, email: str) -> str:
        return email_validator(email)

    @root_validator
    def check_passwords_match(cls, values: dict[str, bool]) -> dict[str, bool]:
        pw1, pw2 = values.get("password"), values.get("password2")

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Пароли не совпадают")

        return values


class AuthorizeSchema(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, email: str) -> str:
        return email_validator(email)
