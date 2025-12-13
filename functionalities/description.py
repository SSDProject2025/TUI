from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.functionalities.description_exception import DescriptionException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        try:
            validate("value", self.value, min_len=1, max_len=1000, custom=pattern(r'[a-zA-Z0-9 ;.,_-]*'))
        except ValidationError:
            raise DescriptionException

    def __str__(self):
        return self.value