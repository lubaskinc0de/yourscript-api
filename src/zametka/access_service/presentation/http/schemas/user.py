from typing import Self

from pydantic import BaseModel, model_validator


class CreateIdentitySchema(BaseModel):
    email: str
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1, pw2 = self.password, self.password2

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Пароли не совпадают")

        return self


class AuthorizeSchema(BaseModel):
    email: str
    password: str
