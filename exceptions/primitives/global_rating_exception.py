class GlobalRatingException(Exception):
    help_message = ("Invalid global rating, it should have an integer part between 0 and 10, a "
                    "decimal part between 0 and 99 and, if the integer part is 10, the decimal "
                    "part can't be different from 0")