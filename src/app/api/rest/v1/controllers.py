from fastapi import APIRouter

from app.api.rest.v1.auth.controllers import router as auth_router
from app.api.rest.v1.health.controllers import router as health_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(health_router, prefix="/health", tags=["Health"])
