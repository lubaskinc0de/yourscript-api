from dataclasses import dataclass
from typing import Literal

Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]


@dataclass
class JWTConfig:
    key: str
    algorithm: Algorithm
