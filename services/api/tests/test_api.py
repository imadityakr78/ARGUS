import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestMockRoutes:
    @pytest.fixture(autouse=True)
    def _enable_mocks(self):
        os.environ["ARGUS_USE_MOCKS"] = "true"

    def test_get_cameras(self):
        response = client.get("/api/cameras")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_events(self):
        response = client.get("/api/events")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_event_by_id(self):
        response = client.get("/api/events/evt_01")
        assert response.status_code == 200
        assert response.json()["eventId"] == "evt_01"

    def test_get_event_not_found(self):
        response = client.get("/api/events/nonexistent")
        assert response.status_code == 404

    def test_get_investigation(self):
        response = client.get("/api/investigations/inv_001")
        assert response.status_code == 200
        data = response.json()
        assert data["investigationId"] == "inv_001"
        assert "hypotheses" in data

    def test_post_investigation(self):
        response = client.post("/api/investigations", json={
            "question": "What happened to the laptop?"
        })
        assert response.status_code == 200

    def test_get_hypotheses(self):
        response = client.get("/api/hypotheses/inv_001")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_camera_graph(self):
        response = client.get("/api/camera-graph")
        assert response.status_code == 200
        data = response.json()
        assert "cameras" in data
