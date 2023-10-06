"""Основной файл приложения."""
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import BALANCE_APP_PORT
from credit_card_balance.src.routers import balance_router, transactions_router
from credit_card_balance.src.routers import readiness


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = '0.0.0.0'   # noqa: F401, S104
    app_port: int = BALANCE_APP_PORT


app = FastAPI()
executor = ProcessPoolExecutor(max_workers=1)

app.include_router(
    balance_router.router,
    prefix='/api',
    tags=['balance'],
)
app.include_router(
    transactions_router.router,
    prefix='/api',
    tags=['transactions'],
)
app.include_router(readiness.router, tags=['readiness'])


if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
