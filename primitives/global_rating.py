from dataclasses import dataclass, InitVar, field
from typing import Any

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.global_rating_exception import GlobalRatingException


@typechecked
@dataclass(frozen=True, order=True)
class GlobalRating:
    value_in_decimals: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()

    def __post_init__(self, create_key):
        validate("create_key", create_key, equals=self.__create_key)
        try:
            validate("value_in_decimals", self.value_in_decimals, min_value=0, max_value=1000)
        except ValidationError:
            raise GlobalRatingException

    def __str__(self):
        return f"{self.value_in_decimals // 100}.{self.value_in_decimals % 1000:02}"

    @staticmethod
    def create(integer: int, decimal: int) -> 'GlobalRating':
        try:
            validate("integer", integer, min_value=0, max_value=10)
            validate("decimal", decimal, min_value=0, max_value=99)

            # if integer == 10 and decimal != 0:
            #     raise ValidationError

            return GlobalRating(decimal + (integer * 100), GlobalRating.__create_key)

        except ValidationError:
            raise GlobalRatingException
