from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_status_main():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_twap_functionality():
    response = client.post("/twap-strategy", json={"symbol": "BTC", "side": "bid", "total_size": 360, "total_time": 3600, "frequency": 30})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == 'done'
    assert response_json['delay'] == 30
    assert response_json['size'] == 3
