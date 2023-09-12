"""Основной файл приложения."""
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import APP_HOST, AUTH_APP_PORT
from credit_card_auth.src.routers import transactions_router, balance_router, token_router
from credit_card_verify.src.routers import verify_router


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = APP_HOST
    app_port: int = AUTH_APP_PORT


app = FastAPI()

app.include_router(token_router.router, prefix='/api', tags=['auth'])
app.include_router(balance_router.router, prefix='/api', tags=['balance'])
app.include_router(
    transactions_router.router,
    prefix='/api',
    tags=['transactions'],
)

if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
