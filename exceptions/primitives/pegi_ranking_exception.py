class PegiRankingException(Exception):
    help_message = "Invalid PEGI ranking: it must be a number included in [3, 7, 12, 16, 18]"