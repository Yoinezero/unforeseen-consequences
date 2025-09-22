from app.domain.exceptions import InfrastructureException


class DatabaseError(InfrastructureException):
    """Wraps a lower-level database exception."""

    def __init__(self, message: str = "A database error occurred.", original_exception: Exception | None = None):
        self.original_exception = original_exception
        super().__init__(message)
