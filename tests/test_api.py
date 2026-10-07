from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Test Workshop",
            "date": "2026-10-07",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total"] == 1
    assert data["status"] == "ACCEPTED"


def test_invalid_email():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Test Workshop",
            "date": "2026-10-07",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_job_not_found():
    response = client.get("/api/jobs/999999")

    assert response.status_code == 404