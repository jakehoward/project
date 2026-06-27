import re
from datetime import datetime

from tasks.task import MAX_ATTR_VALUE_LENGTH, MAX_FILENAME_LEN, Task, TaskMetadata, TaskStatus
from tasks.utils import get_git_user, normalise_name, sanitise_for_single_line


def create_task(name: str, get_who=get_git_user, now=datetime.now) -> Task:
    name_without_newlines = re.sub(r"\n+", " ", name).strip()
    return Task(
        name=name_without_newlines,
        filename=f"{normalise_name(name, MAX_FILENAME_LEN)}.md",
        body=default_template(name=name),
        metadata=TaskMetadata(
            status=TaskStatus.TODO,
            created_at=now(),
            created_by=sanitise_for_single_line(get_who(), max_len=MAX_ATTR_VALUE_LENGTH),
        ),
    )


def default_template(name: str) -> str:
    return f"""
# {name}
""".lstrip()
