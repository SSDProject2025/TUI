class PublisherException(Exception):
    help_message = ("Invalid publisher name: it should be between 1 and 100 characters long and cannot "
                    "have any special character")