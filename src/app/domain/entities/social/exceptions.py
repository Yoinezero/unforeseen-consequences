from app.domain.exceptions import ApplicationException


class SocialProfileAlreadyLinkedError(ApplicationException):
    """Raised when a social profile is already linked to another user."""

    def __init__(self, provider: str):
        self.provider = provider
        super().__init__(f"Use Case Error: This {provider} account is already linked to another user.")
