"""Роутер для верификации пользователя."""
import asyncio
import json
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, Request, status, HTTPException

from config.config import RESPONSE_TIMEOUT
from credit_card_auth.src.schemas.transactions_schemas import (
    VerificationRequest,
)
from credit_card_auth.src.services.handler_utils import oauth2_scheme

router = APIRouter()


@router.post('/verify')
async def verify(   # noqa: WPS210
    card_number: str,
    request: Request,
    selfie: UploadFile = File(...),
    document: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
) -> VerificationRequest:
    """
    Эндпоинт для верификации пользователя.

    Args:
        card_number (str): Номер карты.
        request (Request): Сам запрос из состояния приложения которого мы получаем продюсера.
        selfie (UploadFile): Селфи пользователя.
        document (UploadFile): Документ пользователя.
        token (str): Токен.

    Raises:

    Returns:

    """
    producer = request.app.state.kafka_producer
    pending_requests = request.app.state.pending_requests
    selfie_path = f'photo_storage/{card_number}_selfie_tmp.jpg'
    document_path = f'photo_storage/{card_number}_document_tmp.jpg'

    with open(selfie_path, 'wb') as selfie_buffer:
        selfie_buffer.write(selfie.file.read())

    with open(document_path, 'wb') as doc_buffer:
        doc_buffer.write(document.file.read())

    request_id = uuid.uuid4().hex

    message_data = {
        "request_id": request_id,
        "card_number": card_number,
        "selfie_path": selfie_path,
        "document_path": document_path
    }

    message_data_bytes = json.dumps(message_data).encode('utf-8')
    await producer.send("gran_verify", value=message_data_bytes)

    queue = asyncio.Queue()
    pending_requests[request_id] = queue

    try:
        response = await asyncio.wait_for(
            queue.get(),
            timeout=RESPONSE_TIMEOUT,
        )
        return VerificationRequest(verified=response)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail='Время ожидания ответа от сервиса верификации истекло',
        )


