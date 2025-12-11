import pytest

from exceptions.primitives.pegi_ranking_exception import PegiRankingException
from primitives.pegi import Pegi


def test_pegi_creation_failing_on_invalid_values():
    invalid_values = list(range(-1, 3)) + list(range(4, 7)) + list(range(8, 12)) + list(range(13, 16)) + [17]
    for value in invalid_values:
        with pytest.raises(PegiRankingException):
            Pegi(value)

def test_pegi_creation_successful():
    valid_values = [3, 7, 12, 16, 18]
    for value in valid_values:
        Pegi(value)

def test_pegi_str():
    valid_values = [3, 7, 12, 16, 18]
    for value in valid_values:
        assert str(Pegi(value)) == f"PEGI {value}"