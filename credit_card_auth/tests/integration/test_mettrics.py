"""Тесты на проверку метрик."""
from fastapi.testclient import TestClient

from main_auth import app

client = TestClient(app)

expected_metrics = [
    'gran_request_number',
    'gran_http_requests_total',
    'gran_request_latency_histogram',
    'gran_verification_results_total',
]


def test_metrics_endpoint():
    """Тест на проверку метрик."""
    response = client.get('/metrics')

    assert response.status_code == 200

    for metric in expected_metrics:
        assert metric in response.text, f'Metric {metric} not found in response'    # noqa: E501
