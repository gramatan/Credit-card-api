import time

from fastapi import Request, Response

from prometheus_client import Counter, Histogram
from starlette.status import HTTP_400_BAD_REQUEST


http_requests_total = Counter('http_requests_total', 'Total HTTP Requests')

request_latency_histogram = Histogram(
    'gran_auth_request_latency_histogram',  # Название метрики
    'Request latency.',  # Документация метрики
    ['operation', 'http_status_code', 'error'],  # Лейблы
)


async def metrics_middleware(request: Request, call_next):
    """Middleware для реализации логгирования времени выполнения запроса."""
    start_time = time.monotonic()
    response: Response = await call_next(request)
    operation = f'{request.method} {request.url.path}'
    request_latency_histogram.labels(
        operation,
        response.status_code,
        response.status_code >= HTTP_400_BAD_REQUEST,
    ).observe(
        time.monotonic() - start_time,
    )
    return response
