from fastapi import APIRouter

from app.api.rest.v1.auth.oauth2.controllers import router as oauth2_router

router = APIRouter()

router.include_router(oauth2_router, prefix="/providers")
