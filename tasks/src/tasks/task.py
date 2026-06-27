import re
import subprocess
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


def _normalise_name(name: str) -> str:
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_-]", "__", name)
    name = re.sub(r"___+", "__", name)
    if set(name) == {"_"}:
        raise ValueError("name cannot be normalised - use a-zA-Z0-9 in the task name")
    return name[:MAX_FILENAME_LEN]


def get_git_user() -> str:
    try:
        email = subprocess.check_output(["git", "config", "user.email"], text=True)  # noqa: S607
        name = subprocess.check_output(["git", "config", "user.name"], text=True)  # noqa: S607
        return f"{name} <{email}>"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Unknown"


def sanitise_for_short_single_line(s: str) -> str:
    return s.replace("\n", "")[:MAX_ATTR_VALUE_LENGTH]


def create_task(name: str, get_who=get_git_user, now=datetime.now) -> Task:
    return Task(
        name=name,
        filename=f"{_normalise_name(name)}.md",
        body=default_template(name=name),
        metadata=TaskMetadata(
            status=TaskStatus.TODO,
            created_at=now(),
            created_by=sanitise_for_short_single_line(get_who()),
        ),
    )


def default_template(name: str) -> str:
    return f"""
# {name}
""".lstrip()
