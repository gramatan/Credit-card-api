"""Проверки для кубера."""
from fastapi import APIRouter, status
from starlette.responses import JSONResponse

router = APIRouter()


@router.get(
    '/ready',
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
async def ready():
    """
    Проверка готовности сервиса.

    Returns:
        dict: Статус готовности.
    """
    return {'status': 'ready'}


@router.get(
    '/live',
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
async def live():
    """
    Проверка жизнеспособности сервиса.

    Returns:
        dict: Статус жизнеспособности.
    """
    return {'status': 'alive'}
