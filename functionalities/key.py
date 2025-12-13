from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.functionalities.key_exception import KeyException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Key:
    value: str

    def __post_init__(self):
        try:
            validate("value", self.value, min_len=1, max_len=10, custom=pattern(r'[a-zA-Z0-9_-]*'))
        except ValidationError:
            raise KeyException

    def __str__(self):
        return self.value