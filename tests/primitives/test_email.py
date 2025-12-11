import pytest
from email_validator import EmailNotValidError

from primitives.email import Email

def test_email_creation_failure_on_min_length():
    with pytest.raises(EmailNotValidError):
        Email('')

def test_email_creation_failure_on_max_length():
    with pytest.raises(EmailNotValidError):
        Email('a@' + "a" * 250 + ".com")

def test_email_creation_failure_on_invalid_emails():
    invalid_emails = [
    "test@@example.com",
    "user@",
    "@example.com",
    "user@.com",
    "user@com",
    "user@example..com",
    "user example@example.com",
    "user@exam_ple.com",
    "user@-example.com",
    "user@example-.com",
    "user@example.c",
    "user@[123.456.789.000]"
    ]

    for email in invalid_emails:
        with pytest.raises(EmailNotValidError):
            Email(email)

def test_email_creation_successful():
    Email("domenico@gmail.com")

def test_email_str():
    assert str(Email("domenico@gmail.com")) == "domenico@gmail.com"