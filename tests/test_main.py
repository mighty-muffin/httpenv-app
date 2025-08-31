from app.main import app
from fastapi.testclient import TestClient

# Setup the TestClient
client = TestClient(app)

STATUS_OK = 200


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
