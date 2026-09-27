from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


# ============================================================
# TEST 1 - HOME API
# ============================================================

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


# ============================================================
# TEST 2 - HEALTH API
# ============================================================

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "database" in data


# ============================================================
# TEST 3 - SUMMARY API
# ============================================================

def test_summary():

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_transactions" in data
    assert "normal_transactions" in data
    assert "anomalies_detected" in data

    assert data["total_transactions"] == 998

    assert data["normal_transactions"] == 948

    assert data["anomalies_detected"] == 50


# ============================================================
# TEST 4 - ANOMALIES API
# ============================================================

def test_anomalies():

    response = client.get("/anomalies")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "anomalies" in data

    assert data["count"] == 50

    assert len(data["anomalies"]) == 50


# ============================================================
# TEST 5 - SINGLE ANOMALY
# ============================================================

def test_single_anomaly():

    response = client.get("/anomalies/T0040")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_id"] == "T0040"

    assert data["anomaly_status"] == "ANOMALY"

    assert "anomaly_reason" in data


# ============================================================
# TEST 6 - INVALID TRANSACTION
# ============================================================

def test_invalid_transaction():

    response = client.get("/anomalies/INVALID123")

    assert response.status_code == 404