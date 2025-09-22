from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.rest.controllers import init_routes
from app.containers import Container
from app.infra.middleware.cors import init_cors
from app.lifespan import lifespan


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.add_middleware(SessionMiddleware, secret_key=container.config().app.secret_key)

    init_cors(app)
    init_routes(app)

    return app
