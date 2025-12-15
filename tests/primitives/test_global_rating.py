import pytest
from valid8 import ValidationError

from exceptions.primitives.global_rating_exception import GlobalRatingException
from primitives.global_rating import GlobalRating


def test_global_rating_creation_failed_on_integer():
    with pytest.raises(GlobalRatingException):
        GlobalRating.create(11, 0)

def test_global_rating_creation_failed_on_decimal():
    with pytest.raises(GlobalRatingException):
        GlobalRating.create(10, 100)

def test_global_rating_creation_failed_on_not_calling_create_method():
    with pytest.raises(ValidationError):
        GlobalRating(10, 100)

def test_global_rating_creation_failed_on_last_validation():
    with pytest.raises(GlobalRatingException):
        GlobalRating.create(10, 99)

def test_global_rating_creation_successful():
    GlobalRating.create(10, 00)

def test_global_rating_str():
    assert str(GlobalRating.create(10, 00)) == "10.00"