from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.publisher_exception import PublisherException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Publisher:
    publisher: str

    def __post_init__(self):
        try:
            validate("publisher", self.publisher, min_len=1, max_len=100, custom=pattern(r'[a-zA-Z0-9\s]*'))
        except ValidationError:
            raise PublisherException

    def __str__(self):
        return self.publisher