from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

MAX_ATTR_VALUE_LENGTH = 50
MAX_FILENAME_LEN = 100


class TaskStatus(StrEnum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass(frozen=True)
class TaskMetadata:
    status: TaskStatus
    created_at: datetime
    created_by: str


@dataclass(frozen=True)
class Task:
    filename: str
    name: str
    body: str
    metadata: TaskMetadata
