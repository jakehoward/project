from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from tasks.task import Task, TaskMetadata, TaskStatus


@dataclass(frozen=True)
class HeaderAttrs:
    name: str
    status: TaskStatus
    created_at: datetime
    created_by: str


def _parse_header(raw_file_text: str) -> HeaderAttrs:
    file_text = raw_file_text.strip()

    first_line = file_text.split("\n")[0]
    if set(first_line.strip().replace(" ", "")) != {"-"} or len(first_line.strip()) < 3:
        raise ValueError("Task file must start with header on first line: ---")

    second_dashes_idx = -1
    for idx, line in enumerate(file_text.split("\n")[1:]):
        if line.endswith("---"):  # coupled to how body is parsed
            second_dashes_idx = idx + 1
            break
    if second_dashes_idx == -1:
        raise ValueError("Task file header must close with a: ---")

    header = file_text.split("\n")[1:second_dashes_idx]
    sep = ": "
    header_attrs = {k: v.strip() for k, v in (h.split(sep, 1) for h in header if h.strip() != "")}

    for attr in ["name", "status", "created_at", "created_by"]:
        if not header_attrs.get(attr):
            raise ValueError(f'Task header invalid: missing "{attr}"')

    return HeaderAttrs(
        name=header_attrs["name"],
        status=TaskStatus(header_attrs["status"]),
        created_at=datetime.fromisoformat(header_attrs["created_at"]),
        created_by=header_attrs["created_by"],
    )


def read_task(filepath: Path) -> Task:
    if not filepath.exists():
        raise FileNotFoundError(f"Task not found at: {filepath}")

    text = filepath.read_text()
    header = _parse_header(text)

    sep = "---\n"  # coupled to how header is parsed
    body = sep.join(text.split(sep)[2:])

    return Task(
        filename=filepath.name,
        name=header.name,
        body=body,
        metadata=TaskMetadata(
            status=header.status,
            created_at=header.created_at,
            created_by=header.created_by,
        ),
    )
