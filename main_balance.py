"""Основной файл приложения."""
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI
from jaeger_client import Config
from pydantic_settings import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware

from config.config import BALANCE_APP_PORT
from credit_card_balance.src.middlewares import tracing_middleware
from credit_card_balance.src.routers import (
    balance_router,
    readiness,
    transactions_router,
)


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = '0.0.0.0'   # noqa: F401, S104
    app_port: int = BALANCE_APP_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст для работы приложения.

    В нашем случае используется для Егеря.

    Args:
        app: Приложение.

    Yields:
        Контекст приложения.
    """
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'jaeger-agent.monitoring.svc.cluster.local',   # noqa: E501
                'reporting_port': 6831,
            },
            'logging': True,
        },
        service_name='gran_balance',
        validate=True,
    )
    tracer = config.initialize_tracer()
    yield {'jaeger_tracer': tracer}


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

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=tracing_middleware,
)

if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
