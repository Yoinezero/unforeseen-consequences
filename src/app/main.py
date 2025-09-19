from fastapi import FastAPI

from app.api.rest.controllers import init_routes
from app.containers import Container


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    init_routes(app)
    return app
