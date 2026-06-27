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

    task_path.write_text(task.body, encoding="utf-8")  # todo: move to actions.persist(task)
