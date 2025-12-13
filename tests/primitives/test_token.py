import pytest

from exceptions.primitives.token_exception import TokenException
from primitives.token import Token


def test_token_creation_failure_on_length():
    with pytest.raises(TokenException):
        Token("aB3dE9fGh12IjK4LmN5OpQ6rStUvWxYz7890AbC")

def test_token_creation_failure_on_syntax():
    with pytest.raises(TokenException):
        Token("aB3dE9fGh12IjK4LmN5OpQ6rStUvWxYz7890AbC.")

def test_token_creation_successful():
    Token("aB3dE9fGh12IjK4LmN5OpQ6rStUvWxYz7890AbCd")

def test_token_str():
    assert str(Token("aB3dE9fGh12IjK4LmN5OpQ6rStUvWxYz7890AbCd")) == "aB3dE9fGh12IjK4LmN5OpQ6rStUvWxYz7890AbCd"