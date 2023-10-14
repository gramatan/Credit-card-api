"""Мидлвари с метриками для приложения."""
import time

from fastapi import Request, Response
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)
from prometheus_client import Counter, Histogram
from starlette.status import HTTP_400_BAD_REQUEST

requests_num = Counter(
    'gran_request_number',
    'Count number of requests',
    ['endpoint'],
)
http_requests_total = Counter(
    'gran_http_requests_total',
    'Total HTTP Requests',
)

request_latency_histogram = Histogram(
    'gran_request_latency_histogram',
    'Request latency.',
    ['operation', 'http_status_code', 'error'],
)

verification_results_counter = Counter(
    'gran_verification_results_total',
    'Count verification results',
    ['result'],
)


async def metrics_middleware(request: Request, call_next):
    """
    Middleware для реализации логгирования времени выполнения запроса.

    Args:
        request: Запрос.
        call_next: Следующий обработчик запроса.

    Returns:
        Ответ.
    """
    http_requests_total.inc()
    requests_num.labels(request.url.path).inc()
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


async def tracing_middleware(request: Request, call_next):
    """
    Middleware для реализации трейсинга.

    Args:
        request: Запрос.
        call_next: Следующий обработчик запроса.

    Returns:
        Ответ.
    """
    path = request.url.path
    if (
        path.startswith('/live')
        or path.startswith('/ready')
        or path.startswith('/metrics')
    ):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS,
            request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None

    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: request.url,
    }
    with global_tracer().start_active_span(
        str(request.url.path), child_of=span_ctx, tags=span_tags,
    ):
        return await call_next(request)
