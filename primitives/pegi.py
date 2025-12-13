from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.pegi_ranking_exception import PegiRankingException


@typechecked
@dataclass(frozen=True, order=True)
class Pegi:
    pegi_ranking_int: int

    def __post_init__(self):
        try:
            validate("pegi_ranking_int", self.pegi_ranking_int, is_in=[3, 7, 12, 16, 18])
        except ValidationError:
            raise PegiRankingException()


    def __str__(self):
        return f'PEGI {self.pegi_ranking_int}'
