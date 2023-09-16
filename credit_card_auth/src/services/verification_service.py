"""Verification Service. Will be updated later."""
import asyncio
import json
import uuid

from fastapi import File, Request, UploadFile

from config.config import RESPONSE_TIMEOUT
from credit_card_auth.src.schemas.transactions_schemas import (
    VerificationRequest,
)


class VerificationService:
    """Verification Service."""

    async def verify(
        self,
        card_number: str,
        request: Request,
        selfie: UploadFile = File(...),
        document: UploadFile = File(...),
    ):
        """
        Верификация пользователя.

        Args:
            card_number (str): Номер карты.
            request (Request): Сам запрос для состояний.
            selfie (UploadFile): Селфи пользователя.
            document (UploadFile): Документ пользователя.

        Returns:
            VerificationRequest: Результат верификации.
        """
        selfie_path, document_path = await self._save_uploaded_files(
            card_number,
            selfie,
            document,
        )
        message_data = await self._prepare_message_data(
            card_number,
            selfie_path,
            document_path,
        )
        await self._send_message_to_kafka(request, message_data)
        response = await self._await_response(
            request,
            message_data['request_id'],
        )

        return VerificationRequest(verified=response)

    async def _save_uploaded_files(self, card_number, selfie, document):
        """
        Сохраняем файлы в хранилище.

        Args:
            card_number (str): Номер карты.
            selfie (UploadFile): Селфи пользователя.
            document (UploadFile): Документ пользователя.

        Returns:
            tuple: Пути к файлам.
        """
        selfie_path = f'photo_storage/{card_number}_selfie_tmp.jpg'
        document_path = f'photo_storage/{card_number}_document_tmp.jpg'

        with open(selfie_path, 'wb') as selfie_buffer:
            selfie_buffer.write(selfie.file.read())

        with open(document_path, 'wb') as doc_buffer:
            doc_buffer.write(document.file.read())

        return selfie_path, document_path

    async def _prepare_message_data(
        self,
        card_number,
        selfie_path,
        document_path,
    ):
        """
        Готовим данные для отправки в Kafka.

        Args:
            card_number (str): Номер карты.
            selfie_path (str): Путь к селфи.
            document_path (str): Путь к документу.

        Returns:
            dict: Словарь с данными для отправки в Kafka.
        """
        request_id = uuid.uuid4().hex
        return {
            'request_id': request_id,
            'card_number': card_number,
            'selfie_path': selfie_path,
            'document_path': document_path,
        }

    async def _send_message_to_kafka(self, request, message_data):
        """
        Отправляем данные в кафка.

        Args:
            request (Request): Запрос для состояний.
            message_data (dict): Словарь с данными для отправки в Kafka.
        """
        producer = request.app.state.kafka_producer
        message_data_bytes = json.dumps(message_data).encode('utf-8')
        await producer.send('gran_verify', value=message_data_bytes)

    async def _await_response(self, request, request_id):
        """Слушаем ответ от Kafka.

        Args:
            request (Request): Запрос для состояний.
            request_id (str): ID запроса.

        Returns:
            bool: Результат верификации.
        """
        pending_requests = request.app.state.pending_requests
        queue = asyncio.Queue()  # type: ignore
        pending_requests[request_id] = queue
        return await asyncio.wait_for(queue.get(), timeout=RESPONSE_TIMEOUT)
