"""Мидлвари с егерем для приложения."""
from fastapi import Request
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)


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
