from dataclasses import dataclass
from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.token_exception import TokenException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Token:
    token: str

    def __post_init__(self):
        try:
            validate("token", self.token, min_len=40, max_len=40, custom=pattern(r'[a-zA-Z0-9]*'))
        except ValidationError:
            raise TokenException

    def __str__(self):
        return self.token