class GameDescriptionException(Exception):
    help_message = ('Invalid Game Description: it should be between 1 and 200 characters and cannot include '
                    'special characters other than [!,;:.?\'"()-]')