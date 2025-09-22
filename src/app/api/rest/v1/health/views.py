"""Health check Pydantic models and schemas."""

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Schema for health status response."""

    status: str
    environment: str
    app_name: str


class ReadinessStatus(BaseModel):
    """Schema for readiness status response."""

    status: str


class LivenessStatus(BaseModel):
    """Schema for liveness status response."""

    status: str
