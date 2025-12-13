class KeyException(Exception):
    help_message = ("Invalid key: it should be between 1 and 10 characters long and should contain "
                    "only characters in [a-zA-Z0-9_-]")