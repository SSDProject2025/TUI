import pytest

from exceptions.primitives.rating_count_exception import RatingCountException
from primitives.ranting_count import RatingCount


def test_rating_count_creation_failed_on_min_value():
    with pytest.raises(RatingCountException):
        RatingCount(-1)

def test_rating_count_creation_successful():
    RatingCount(1)

def test_rating_count_str():
    assert str(RatingCount(1)) == "1"