import uuid

import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.infra.db.base import BaseModel
from app.infra.db.constants import DEFAULT_USER_SETTINGS
from app.infra.db.mixins import TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, BaseModel):
    """User model."""

    __tablename__ = "users"

    email: orm.Mapped[str] = orm.mapped_column(unique=True, index=True)
    settings: orm.Mapped[dict] = orm.mapped_column(default=DEFAULT_USER_SETTINGS)
    is_active: orm.Mapped[bool] = True


class SocialProfile(UUIDMixin, TimestampMixin, BaseModel):
    """Linked social networks model."""

    __tablename__ = "social_profiles"

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(sa.ForeignKey("users.id"), onupdate="CASCADE")
    social_id: orm.Mapped[str | None]
    provider: orm.Mapped[str]
