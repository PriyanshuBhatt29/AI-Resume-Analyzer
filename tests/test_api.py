from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_text_rejects_short_input():
    response = client.post("/api/analyze-text", json={"resume_text":"too short","job_description":"also too short"})
    assert response.status_code == 422
