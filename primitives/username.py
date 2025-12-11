from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.username_exception import UsernameException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    username: str

    def __post_init__(self):
        try:
            validate("username", self.username, min_len=1, max_len=150, custom=pattern(r'[a-zA-Z0-9_@+.-]*'))
        except ValidationError:
            raise UsernameException

    def __str__(self):
        return self.username