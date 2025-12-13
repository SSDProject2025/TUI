import pytest

from exceptions.primitives.publisher_exception import PublisherException
from primitives.publisher import Publisher


def test_publisher_creation_failed_on_min_length():
    with pytest.raises(PublisherException):
        Publisher("")

def test_publisher_creation_failed_on_max_length():
    with pytest.raises(PublisherException):
        Publisher("a" * 101)

def test_publisher_creation_failed_on_invalid_name():
    with pytest.raises(PublisherException):
        Publisher("Konami.")

def test_publisher_creation_successful():
    Publisher("Konami")

def test_publisher_str():
    assert str(Publisher("Konami")) == "Konami"