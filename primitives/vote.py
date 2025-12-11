from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.vote_exception import VoteException


@typechecked
@dataclass(frozen=True, order=True)
class Vote:
    vote: int

    def __post_init__(self):
        try:
            validate("vote", self.vote, min_value=1, max_value=10)
        except ValidationError:
            raise VoteException

    def __str__(self):
        return str(self.vote)