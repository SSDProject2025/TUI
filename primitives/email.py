from dataclasses import dataclass

from typeguard import typechecked
from email_validator import validate_email

@typechecked
@dataclass(frozen=True, order=True)
class Email:
    email: str

    def __post_init__(self):
        validate_email(self.email)

    def __str__(self):
        return self.email