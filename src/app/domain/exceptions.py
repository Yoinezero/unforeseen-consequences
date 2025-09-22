class AppException(Exception):
    """Base exception for the entire application."""

    @property
    def message(self) -> str:
        return self.args[0] if self.args else "An application error occurred."


class ApplicationException(AppException):
    """Base for exceptions related to application service logic (use cases)."""

    pass


class InfrastructureException(AppException):
    """Base for exceptions related to external services (DB, APIs, etc.)."""

    pass


class DomainException(AppException):
    """Base for exceptions related to business logic and rules (invariants)."""

    pass
