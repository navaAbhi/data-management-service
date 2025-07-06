from enum import Enum


class ImportJobStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    COMPLETED = "COMPLETED"
