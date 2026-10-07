from pathlib import Path

from app.services.certificate_generator import generate_certificate


def test_generate_certificate():

    file_path = generate_certificate(
        certificate_id=9999,
        recipient_name="Test User",
        event_name="Test Workshop",
        event_date="2026-10-07"
    )

    assert Path(file_path).exists()
    assert file_path.endswith(".pdf")

    Path(file_path).unlink()