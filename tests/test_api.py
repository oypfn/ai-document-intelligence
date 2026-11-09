from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rejects_non_pdf() -> None:
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_rejects_invalid_pdf_signature() -> None:
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": ("broken.pdf", b"not a pdf", "application/pdf")},
    )
    assert response.status_code == 400


def test_rejects_files_over_ten_megabytes() -> None:
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": ("large.pdf", b"%PDF-" + b"x" * (10 * 1024 * 1024), "application/pdf")},
    )
    assert response.status_code == 413
