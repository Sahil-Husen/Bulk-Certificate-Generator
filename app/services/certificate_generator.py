from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    event_name: str,
    event_date: str
) -> str:

    filename = f"certificate_{certificate_id}.pdf"
    file_path = GENERATED_DIR / filename

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4

    # Border
    pdf.rect(
        40,
        40,
        width - 80,
        height - 80
    )

    # Title
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "CERTIFICATE"
    )

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 200,
        "OF PARTICIPATION"
    )

    # Main text
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 280,
        "This is to certify that"
    )

    # Recipient
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(
        width / 2,
        height - 330,
        recipient_name
    )

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 390,
        "has successfully participated in"
    )

    # Event
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 430,
        event_name
    )

    # Date
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        150,
        f"Date: {event_date}"
    )

    # Signature
    pdf.line(
        width / 2 - 70,
        100,
        width / 2 + 70,
        100
    )

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        80,
        "Authorized Signature"
    )

    pdf.save()

    return str(file_path)