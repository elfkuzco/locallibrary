class RecordDoesNotExistError(Exception):
    """A database record does not exist."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
