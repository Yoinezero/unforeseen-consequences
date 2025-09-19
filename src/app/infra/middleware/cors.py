from typing import TYPE_CHECKING

from starlette.middleware.cors import CORSMiddleware

if TYPE_CHECKING:
    from fastapi import FastAPI


def init_cors(
    app: "FastAPI",
    allow_origins: tuple[str] = ("*",),
    allow_headers: tuple[str] = ("*",),
    allow_methods: tuple[str] = ("*",),
    allow_credentials: bool = True,
) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )
