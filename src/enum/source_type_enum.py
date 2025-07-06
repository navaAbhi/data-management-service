from enum import Enum


class SourceType(str, Enum):
    LOCAL = "local"
    LINK = "link"
    CLOUD = "cloud"
