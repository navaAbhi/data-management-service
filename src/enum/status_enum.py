from enum import Enum


class ImportJobStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    QUEUED = "QUEUED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
