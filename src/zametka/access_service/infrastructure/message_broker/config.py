from dataclasses import dataclass


@dataclass
class AMQPConfig:
    host: str = "localhost"
    port: int = 5672
    login: str = "guest"
    password: str = "guest"
