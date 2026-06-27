from tasks.config import read_config
from tasks.task import Task


def create_header(task: Task) -> str:
    lines = [
        "---",
        f"name: {task.name}",
        f"status: {task.metadata.status}",
        f"created_by: {task.metadata.created_by}",
        f"created_at: {task.metadata.created_at}",
        "---",
    ]
    return "\n".join(lines)


def persist_task(task: Task) -> None:
    config = read_config()
    if not config:
        raise RuntimeError(f"Could not read config when writing task {task.filename}")
    header = create_header(task)
    (config.tasks_dir / task.filename).write_text(header + "\n" + task.body)
