from fastapi import FastAPI

from .auth import auth_router
from .db import db_router
from .query import query_router

def get_core_app():
    """Initialize the core application."""
    app = FastAPI()

    app.include_router(auth_router)
    app.include_router(db_router)
    app.include_router(query_router)

    return app

core_app = get_core_app()