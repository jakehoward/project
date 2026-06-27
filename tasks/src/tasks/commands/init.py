from dataclasses import dataclass
from pathlib import Path

from tasks.config import Config, get_config_path, read_config, write_config


@dataclass(frozen=True)
class InitResult:
    tasks_dir: Path
    config_file: Path


def init(tasks_dir: Path) -> InitResult:
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
    return InitResult(tasks_dir=resolved_tasks_dir, config_file=get_config_path())
