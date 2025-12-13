import pytest

from exceptions.functionalities.description_exception import DescriptionException
from functionalities.description import Description


def test_description_creation_failed_on_min_length():
    with pytest.raises(DescriptionException):
        Description("")

def test_description_creation_failed_on_max_length():
    with pytest.raises(DescriptionException):
        Description("a" * 1001)

def test_description_creation_successful():
    Description("a-zA-Z0-9 ;.,_-")

def test_description_str():
    assert str(Description("a-zA-Z0-9 ;.,_-")) == "a-zA-Z0-9 ;.,_-"