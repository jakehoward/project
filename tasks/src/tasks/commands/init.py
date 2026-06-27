from pathlib import Path

from tasks.config import Config, read_config, write_config


def init(tasks_dir: Path) -> None:
    resolved_tasks_dir = tasks_dir.resolve()
    if not resolved_tasks_dir.is_relative_to(Path.cwd()):
        raise ValueError("Tasks dir must be inside the current working directory")

    config = read_config()
    if config:
        raise FileExistsError(
            f'Init Error: Config already exists. Tasks dir set to: "{config.tasks_dir}"'
        )
    if tasks_dir.exists():
        raise FileExistsError(
            f"Init Error: tasks dir already exists: {resolved_tasks_dir.relative_to(Path.cwd())}"
        )

    write_config(Config(tasks_dir=resolved_tasks_dir.relative_to(Path.cwd())))
    tasks_dir.mkdir(parents=True)
    (tasks_dir / ".gitkeep").touch()
