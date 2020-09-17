from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller import base, checks
from middleware import connection


def register_controllers(app: FastAPI) -> None:
    """
    register controller callbacks to routers
    """
    app.include_router(base.router)
    app.include_router(checks.router, prefix="/checks", tags=["checks"])


def register_middlewares(app: FastAPI) -> None:
    """
    register middlewares
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware('http')(connection.calc_time)
