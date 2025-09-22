import uuid_utils as uuid

from pydantic import UUID7, EmailStr, Field, field_validator

from app.domain.entities.base import BaseEntity
from app.domain.entities.user.constants import DEFAULT_USER_SETTINGS
from app.domain.entities.user.exceptions import InvalidEmailError


class UserEntity(BaseEntity):
    """
    A Pydantic-based entity for a User.
    It is immutable and self-validating.
    """

    id: UUID7 = Field(default_factory=uuid.uuid7)
    email: EmailStr
    settings: dict = DEFAULT_USER_SETTINGS

    is_active: bool = True

    def change_email(self, email: str) -> "UserEntity":
        try:
            EmailStr._validate(email)
            return self.update_model(update={"email": email})
        except ValueError as e:
            raise InvalidEmailError(user_id=self.id, email=email) from e

    def update_settings(self, settings: dict) -> "UserEntity":
        new_settings = self.settings | settings
        return self.update_model(update={"settings": new_settings})

    def deactivate(self) -> "UserEntity":
        if not self.is_active:
            raise ValueError("User is already inactive.")

        return self.update_model(update={"is_active": False})

    def activate(self) -> "UserEntity":
        if self.is_active:
            raise ValueError("User is already active.")

        return self.update_model(update={"is_active": True})
