"""Основной файл приложения."""
import asyncio
from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI
from jaeger_client import Config
from prometheus_client import make_asgi_app
from pydantic_settings import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from config.config import AUTH_APP_PORT, PATH_PREFIX
from config.kafka_setup import (
    kafka_response_listener,
    start_producer,
    stop_producer,
)
from credit_card_auth.src.middlewares import (
    metrics_middleware,
    tracing_middleware,
)
from credit_card_auth.src.routers import (
    balance_router,
    readiness,
    token_router,
    transactions_router,
    verification_router,
)


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = '0.0.0.0'   # noqa: F401, S104
    app_port: int = AUTH_APP_PORT


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
    session = ClientSession()
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
        service_name='gran_auth',
        validate=True,
    )
    tracer = config.initialize_tracer()
    yield {'client_session': session, 'jaeger_tracer': tracer}
    await session.close()


app = FastAPI(lifespan=lifespan)


@app.on_event('startup')
async def startup_event():
    """Начало работы приложения."""
    app.state.kafka_producer = await start_producer()
    app.state.pending_requests = {}
    asyncio.create_task(kafka_response_listener(app))


@app.on_event('shutdown')
async def shutdown_event():
    """Окончание работы приложения."""
    await stop_producer(app.state.kafka_producer)


app.include_router(token_router.router, prefix=PATH_PREFIX, tags=['auth'])
app.include_router(balance_router.router, prefix=PATH_PREFIX, tags=['balance'])
app.include_router(
    verification_router.router,
    prefix=PATH_PREFIX,
    tags=['verification'],
)
app.include_router(
    transactions_router.router,
    prefix=PATH_PREFIX,
    tags=['transactions'],
)
app.include_router(readiness.router, tags=['readiness'])

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)
app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
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
