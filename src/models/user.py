from src.models.base import Base
from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    credentials = relationship(
        "Credential", back_populates="user", cascade="all, delete")
    import_jobs = relationship(
        "ImportJob", back_populates="user", cascade="all, delete")
