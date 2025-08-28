from fastapi.testclient import TestClient
from app.main import app

# Setup the TestClient
client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Hello, World!"


def test_hello_name():
    response = client.get("/?name=Test")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Hello, Test!"


def test_bye():
    response = client.get("/bye")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Goodbye, World!"


def test_bye_name():
    response = client.get("/bye?name=Test")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == "Goodbye, Test!"
