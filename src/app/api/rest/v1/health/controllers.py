"""Health check router."""

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.rest.v1.health.views import HealthStatus, LivenessStatus, ReadinessStatus
from app.config.settings import Settings
from app.containers import Container

router = APIRouter()


@router.get(
    "/",
    summary="Health Check",
    description="Basic health check endpoint for monitoring.",
    response_description="Application health status and environment info",
)
@inject
async def health_check(
    settings: Annotated[Settings, Depends(Provide[Container.config])],
) -> HealthStatus:
    """Basic health check endpoint."""
    return HealthStatus(
        status="healthy",
        environment=settings.app.environment,
        app_name=settings.app.name,
    )


@router.get(
    "/ready",
    summary="Readiness Check",
    description="Readiness check for Kubernetes/Docker deployments.",
    response_description="Application readiness status",
)
async def readiness_check() -> ReadinessStatus:
    """Readiness check for Kubernetes/Docker."""
    return ReadinessStatus(status="ready")


@router.get(
    "/live",
    summary="Liveness Check",
    description="Liveness check for Kubernetes/Docker deployments.",
    response_description="Application liveness status",
)
async def liveness_check() -> LivenessStatus:
    """Liveness check for Kubernetes/Docker."""
    return LivenessStatus(status="alive")
