from typing import Any

from pydantic import UUID7, BaseModel, EmailStr


class UserView(BaseModel):
    id: UUID7
    email: EmailStr
    settings: dict[str, Any]
    is_active: bool
