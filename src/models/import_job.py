from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from src.models.base import Base


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)
    source_type = Column(String, nullable=False)
    source_details = Column(JSON, nullable=True)
    status = Column(String, default="PENDING")
    progress_percentage = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="import_jobs")
    files = relationship(
        "File", back_populates="import_job", cascade="all, delete")
