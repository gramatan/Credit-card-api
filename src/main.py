"""Основной файл приложения."""
from fastapi import FastAPI

from src.routers import balance_router, token_router

app = FastAPI()

app.include_router(token_router.router, prefix='/api', tags=['auth'])
app.include_router(balance_router.router, prefix='/api', tags=['balance'])
