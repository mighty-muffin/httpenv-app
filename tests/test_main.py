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


def test_hello_formal():
    response = client.get('/?formal=True')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Good day to you, World.'


def test_goodbye():
    response = client.get('/goodbye')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Goodbye, World!'


def test_goodbye_name():
    response = client.get('/goodbye?name=Test')
    assert response.status_code == STATUS_OK, response.text
    data = response.json()
    assert data == 'Goodbye, Test!'
