class DescriptionException(Exception):
    help_message = ("Invalid description: it should be between 1 and 1000 characters long and should contain "
                    "only characters in [a-zA-Z0-9 ;.,_-]")