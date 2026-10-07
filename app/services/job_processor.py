from datetime import datetime

from app.database import SessionLocal
from app.models.job import GenerationJob
from app.models.certificate import Certificate
from app.services.certificate_generator import generate_certificate


def process_job(job_id: int):

    db = SessionLocal()

    try:
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        certificates = db.query(Certificate).filter(
            Certificate.job_id == job_id
        ).all()

        for certificate in certificates:

            try:
                certificate.status = "PROCESSING"
                db.commit()
                 
                file_path = generate_certificate(
                    certificate.id,
                    certificate.recipient_name,
                    job.event_name,
                    job.event_date
                )

                certificate.status = "SUCCESS"
                certificate.file_path = file_path

                job.successful += 1

                db.commit()

            except Exception as error:

                certificate.status = "FAILED"
                certificate.error_message = str(error)

                job.failed += 1

                db.commit()

        job.status = "COMPLETED"
        job.completed_at = datetime.utcnow()

        db.commit()

    except Exception:

        job.status = "FAILED"
        db.commit()

    finally:
        db.close()