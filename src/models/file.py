from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from src.models.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    import_job_id = Column(UUID(as_uuid=True), ForeignKey(
        "import_jobs.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))

    import_job = relationship("ImportJob", back_populates="files")
    file_metadata = relationship("FileMetadata", uselist=False,
                            back_populates="file", cascade="all, delete")
