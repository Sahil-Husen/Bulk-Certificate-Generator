from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone

from app.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )

    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)

    status = Column(
        String,
        default="PENDING",
        nullable=False
    )

    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )