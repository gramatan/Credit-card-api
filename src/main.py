"""Основной файл приложения."""
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI

from src.routers import balance_router, token_router, transactions_router

app = FastAPI()
executor = ProcessPoolExecutor(max_workers=1)

app.include_router(token_router.router, prefix='/api', tags=['auth'])
app.include_router(balance_router.router, prefix='/api', tags=['balance'])
app.include_router(
    transactions_router.router,
    prefix='/api',
    tags=['transactions'],
)
