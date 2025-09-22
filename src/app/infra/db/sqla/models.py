import uuid

from typing import Any

import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.infra.db.sqla.base import BaseModel
from app.infra.db.sqla.mixins import TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, BaseModel):
    """User model."""

    __tablename__ = "users"

    email: orm.Mapped[str] = orm.mapped_column(unique=True, index=True)
    settings: orm.Mapped[dict[str, Any]]
    is_active: orm.Mapped[bool] = True

    social_profiles = orm.relationship(
        "SocialProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise",
    )


class SocialProfile(UUIDMixin, TimestampMixin, BaseModel):
    """Linked social networks model."""

    __tablename__ = "social_profiles"
    __table_args__ = (sa.UniqueConstraint("provider", "provider_user_id"),)

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(sa.ForeignKey("users.id"))
    provider: orm.Mapped[str] = orm.mapped_column(unique=True, index=True)
    provider_user_id: orm.Mapped[str]

    user = orm.relationship(
        "User",
        back_populates="social_profiles",
        lazy="raise",
    )
