from app.domain.exceptions import ApplicationException, DomainException


class UserAlreadyInactiveError(DomainException):
    """Raised when trying to deactivate an already inactive user."""

    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"Domain Rule Violation: User {user_id} is already inactive.")


class InvalidEmailError(DomainException):
    """Raised when trying to use invalid string as an email."""

    def __init__(self, user_id, email):
        self.user_id = user_id
        super().__init__(f"Domain Rule Violation: Cannot use {email} as an email for user {user_id}.")


class UserNotFoundError(ApplicationException):
    """Raised when a user is not found by an application service."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Use Case Error: User with identifier '{identifier}' not found.")
