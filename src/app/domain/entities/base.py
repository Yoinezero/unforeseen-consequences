from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    updated_at: datetime = datetime.now(timezone.utc)
    created_at: datetime = datetime.now(timezone.utc)

    def update_model(self, update: dict):
        update["updated_at"] = datetime.now(timezone.utc)
        return self.model_copy(update=update)
