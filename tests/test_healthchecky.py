from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

STATUS_OK = 200

def test_healthcheck_success():
    response = client.get('/healthcheck')
    assert response.status_code == STATUS_OK
    assert response.json() == {'status': 'OK'}
