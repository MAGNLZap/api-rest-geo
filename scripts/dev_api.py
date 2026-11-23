from fastapi import FastAPI


def create_app() -> FastAPI:
    from app.config import settings

    settings.ENVIRONMENT = "development"
    settings.ROOT_PATH = ""

    from app.main import app

    return app
