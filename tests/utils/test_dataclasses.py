import pytest
from dataclasses import dataclass

from typeguard import TypeCheckError

from utils.dataclasses import validate_dataclass


@dataclass
class ValidExample:
    a: int
    b: str


@dataclass
class InvalidExample:
    a: int
    b: str


def test_validate_dataclass_with_valid_types():
    obj = ValidExample(a=10, b="hello")
    validate_dataclass(obj)


def test_validate_dataclass_with_invalid_types():
    obj1 = InvalidExample(a="not an int", b="hello")
    obj2 = InvalidExample(a=4, b=5)
    objects = [obj1, obj2]
    for obj in objects:
        with pytest.raises(TypeCheckError):
            validate_dataclass(obj)
