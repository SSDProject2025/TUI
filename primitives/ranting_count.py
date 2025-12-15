from dataclasses import dataclass

from valid8 import validate, ValidationError
from typeguard import typechecked

from exceptions.primitives.rating_count_exception import RatingCountException


@typechecked
@dataclass(frozen=True, order=True)
class RatingCount:
    count: int

    def __post_init__(self):
        try:
            validate("count", self.count, min_value=0)
        except ValidationError:
            raise RatingCountException

    def __str__(self):
        return str(self.count)
