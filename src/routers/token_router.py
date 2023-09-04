"""Роутер для работы с токенами."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.schemas.token_schemas import TokenData
from src.services.token_service import TokenService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


@router.post('/auth', response_model=TokenData)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: TokenService = Depends(),
) -> TokenData:
    """
    Получение токена.

    Args:
        form_data (OAuth2PasswordRequestForm): Данные формы.
        response (TokenService): Сервис для работы с токенами.

    Returns:
        TokenData: Токен.
    """
    return await response.get_token(form_data)

