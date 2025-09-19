from typing import Any

from sqlalchemy import JSON, MetaData
from sqlalchemy.orm import DeclarativeBase

from app.infra.db.constants import POSTGRES_INDEXES_NAMING_CONVENTION

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class BaseModel(DeclarativeBase):
    """Inherit from Declarative base."""

    metadata = metadata
    type_annotation_map = {dict[str, Any]: JSON}
