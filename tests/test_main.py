from app.main import app
from fastapi.testclient import TestClient

# Setup the TestClient
client = TestClient(app)

STATUS_OK = 200
STATUS_SERVICE_UNAVAILABLE = 503


def test_hello():
    response = client.get('/')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Hello, World!'


def test_hello_name():
    response = client.get('/?name=Test')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Hello, Test!'


def test_bye():
    response = client.get('/bye')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Goodbye, World!'


def test_bye_name():
    response = client.get('/bye?name=Test')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Goodbye, Test!'


def test_policeducode_serves_the_exposed_value_without_caching(infisical):
    response = client.get('/policeducode')

    assert response.status_code == STATUS_OK, response.text
    assert response.headers['cache-control'] == 'no-store'
    assert response.json() == {
        'value': 'first',
        'environment': 'staging',
        'rotated_at': '2026-11-24T12:00:00Z',
        'version': '1.2.3',
        'stale': False,
    }


def test_policeducode_is_unavailable_before_the_first_successful_fetch(infisical):
    infisical.fail_fetch = True

    response = client.get('/policeducode')

    assert response.status_code == STATUS_SERVICE_UNAVAILABLE
    assert response.headers['cache-control'] == 'no-store'


def test_policeducode_serves_the_last_value_marked_stale_during_an_outage(
    infisical, clock
):
    client.get('/policeducode')

    infisical.fail_fetch = True
    clock.advance(120)
    response = client.get('/policeducode')

    assert response.status_code == STATUS_OK, response.text
    assert response.json()['value'] == 'first'
    assert response.json()['stale'] is True
