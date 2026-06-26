import re

from tasks.config import assert_initialised, read_config


def _normalise_name(name: str) -> str:
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_-]", "__", name)
    name = re.sub(r"___+", "__", name)
    if set(name) == {"_"}:
        raise ValueError("name cannot be normalised - use a-zA-Z0-9 in the task name")
    return name


def add(name: str) -> None:
    assert_initialised()
    if not name:
        raise ValueError("Add task must provide a name")

    config = read_config()
    if not config:
        raise RuntimeError("Could not read config when adding task")

    normalised_name = _normalise_name(name)
    task_path = config.tasks_dir.resolve() / f"{normalised_name}.md"
    if task_path.exists():
        raise ValueError(f"Task with name {normalised_name} already exists")

    task_path.write_text(f"# {name}", encoding="utf-8")
