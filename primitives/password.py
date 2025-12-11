from dataclasses import dataclass
from typeguard import typechecked
from valid8 import validate

from exceptions.primitives.password_exception import PasswordException

@typechecked
@dataclass(frozen=True, order=True)
class Password:
    password: str

    def __post_init__(self):
        try:
            validate("password", self.password, min_len=8)
        except:
            raise PasswordException

    def __str__(self) -> str:
        return self.password