"""Основной файл приложения."""
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import APP_HOST, VERIFICATION_APP_PORT
from credit_card_verify.src.routers import verify_router


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = APP_HOST
    app_port: int = VERIFICATION_APP_PORT


app = FastAPI()
executor = ProcessPoolExecutor(max_workers=1)

app.include_router(verify_router.router, prefix='/api', tags=['verify'])

if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
