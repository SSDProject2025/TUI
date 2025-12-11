class UsernameException(Exception):
    help_message = ("Invalid username: it should have between 1 and 150 characters and can include numbers and "
                    "special characters in [_@+.-]")