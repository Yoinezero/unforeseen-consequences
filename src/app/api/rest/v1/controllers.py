from fastapi import APIRouter

from app.api.rest.v1.auth.controllers import router as auth_router
from app.api.rest.v1.health.controllers import router as health_router
from app.api.rest.v1.users.controllers import router as users_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(users_router, prefix="/users", tags=["Users"])
