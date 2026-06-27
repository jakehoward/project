from pathlib import Path

from tasks import actions
from tasks.actions import create_task
from tasks.config import assert_initialised, read_config


def add_task(name: str) -> None:
    if not name:
        raise ValueError("Add task must provide a name")

    assert_initialised()

    config = read_config()
    if not config:
        raise RuntimeError("Could not read config when adding task")

    task = create_task(name)
    task_path = config.tasks_dir.resolve() / task.filename
    if task_path.exists():
        raise ValueError(f"Task with filename {task.filename} already exists")

    actions.persist_task(task)
    print(
        f"Added task:\n"
        f'    name:   "{task.name}"\n'
        f'    file:   "{task_path.relative_to(Path.cwd())}"\n'
        f'    status: "{task.metadata.status}"\n'
        f'    author: "{task.metadata.created_by}"'
    )
