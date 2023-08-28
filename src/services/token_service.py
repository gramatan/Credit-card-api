

class TokenService:
    """Сервис для работы с токенами."""

    def __init__(
        self,
    ):
        """
        Инициализация сервиса.

        Args:
            db (Session): Сессия БД.
        """
        self.db = db

    def get_token(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ) -> TokenData:
        """
        Получение токена.

        Args:
            form_data (OAuth2PasswordRequestForm): Данные формы.

        Returns:
            TokenData: Токен.
        """
        user = get_user_by_username(self.db, form_data.username)
        if not user:
            raise_unauthorized_exception('Incorrect username or password')
        if not verify_password(form_data.password, user.hashed_password):
            raise_unauthorized_exception('Incorrect username or password')

        access_token_expires = timedelta(minutes=TOKEN_TTL)
        access_token = create_access_token(
            token_data={'sub': user.username},
            expires_delta=access_token_expires,
        )

        return TokenData(   # noqa: S106
            access_token=access_token,
            token_type='bearer',
        )
