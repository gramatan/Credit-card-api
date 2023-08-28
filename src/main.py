"""Основной файл приложения."""
from fastapi import FastAPI

from src.routers import token_router

app = FastAPI()

app.include_router(token_router.router, tags=['token'])
