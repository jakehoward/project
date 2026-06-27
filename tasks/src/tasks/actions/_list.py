from tasks import actions
from tasks.config import read_config
from tasks.task import Task


def list_tasks() -> list[Task]:
    config = read_config()
    if not config:
        raise RuntimeError("No config file found. Maybe you need to run `tasks init`?")

    md_files = list(config.tasks_dir.glob("*.md"))
    tasks = []
    for md_file in md_files:
        # read_task can error, rather that than silently swallow tasks for now
        task = actions.read_task(md_file)
        tasks.append(task)
    return sorted(tasks, key=lambda task: task.metadata.created_at, reverse=True)
