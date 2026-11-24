from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

STATUS_OK = 200
STATUS_SERVICE_UNAVAILABLE = 503


def test_healthy_after_a_successful_fetch(infisical):
    response = client.get('/healthcheck')
    assert response.status_code == STATUS_OK
    assert response.json() == {'status': 'OK'}


def test_unhealthy_before_any_successful_fetch(infisical):
    infisical.fail_fetch = True

    response = client.get('/healthcheck')

    assert response.status_code == STATUS_SERVICE_UNAVAILABLE


def test_healthy_while_stale_for_less_than_five_minutes(infisical, clock):
    client.get('/healthcheck')

    infisical.fail_fetch = True
    clock.advance(4 * 60 + 59)
    response = client.get('/healthcheck')

    assert response.status_code == STATUS_OK


def test_unhealthy_once_stale_for_more_than_five_minutes(infisical, clock):
    client.get('/healthcheck')

    infisical.fail_fetch = True
    clock.advance(5 * 60 + 1)
    response = client.get('/healthcheck')

    assert response.status_code == STATUS_SERVICE_UNAVAILABLE


def test_healthcheck_after_the_cache_window_refreshes_from_infisical(infisical, clock):
    client.get('/healthcheck')

    clock.advance(60)
    client.get('/healthcheck')

    assert len(infisical.fetches) == 2  # noqa: PLR2004
