from typing import TYPE_CHECKING

from app.api.rest.v1.controllers import router as v1_router

if TYPE_CHECKING:
    from fastapi import FastAPI


def init_routes(app: "FastAPI") -> None:
    app.include_router(
        v1_router,
        prefix="/v1",
    )
