from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)

    status = Column(
        String,
        default="PENDING",
        nullable=False
    )

    total = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )