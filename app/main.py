from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.services.job_processor import process_job


from app.database import engine, Base, get_db
from app.models.job import GenerationJob
from app.models.certificate import Certificate
from app.schemas.job import GenerationRequest


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for generating certificates in bulk",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.post("/api/jobs")
def create_job(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    job = GenerationJob(
        event_name=request.event_name,
        event_date=str(request.date),
        total=len(request.recipients),
        status="PENDING"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    background_tasks.add_task(
        process_job,
        job.id
    )

    return {
    "job_id": job.id,
    "status": "ACCEPTED",
    "total": job.total
}
    
@app.get("/api/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    progress = 0

    if job.total > 0:
        progress = round(
            ((job.successful + job.failed) / job.total) * 100,
            2
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
        "progress": progress
    }
    
@app.get("/api/jobs/{job_id}/certificates")
def get_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    certificates = db.query(Certificate).filter(
        Certificate.job_id == job_id
    ).all()

    return {
        "job_id": job_id,
        "certificates": [
            {
                "id": certificate.id,
                "recipient_name": certificate.recipient_name,
                "recipient_email": certificate.recipient_email,
                "status": certificate.status,
                "download_url": (
                    f"/api/certificates/{certificate.id}"
                    if certificate.status == "SUCCESS"
                    else None
                ),
                "error": certificate.error_message
            }
            for certificate in certificates
        ]
    }
    
@app.get("/api/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate was not generated successfully"
        )

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"{certificate.recipient_name}_certificate.pdf"
    )