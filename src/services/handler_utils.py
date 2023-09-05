"""Утилиты для роутеров."""
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth')


def raise_unauthorized_exception(detail: str) -> None:
    """
    Возвращает 401 ошибку с сообщением об ошибке.

    Args:
        detail (str): Сообщение об ошибке.

    Raises:
        HTTPException: 401 ошибка с сообщением об ошибке.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={'WWW-Authenticate': 'Bearer'},
    )
