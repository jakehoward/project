from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILENAME = ".tasks.toml"


@dataclass(frozen=True)
class Config:
    tasks_dir: Path


def _assert_tasks_dir_path_is_valid(tasks_dir: Path) -> None:
    path_string = str(tasks_dir)
    if '"' in path_string:
        raise ValueError(
            f"Invalid Config: 'tasks_dir' path cannot contain double quote: {path_string}"
        )


def read_config() -> Config | None:
    if Path(CONFIG_FILENAME).exists():
        with open(CONFIG_FILENAME, "rb") as f:
            config = tomllib.load(f)

        if "tasks_dir" not in config:
            raise ValueError(f"Invalid Config: 'tasks_dir' is missing in {CONFIG_FILENAME}")
        if not Path(config["tasks_dir"]).resolve().is_relative_to(Path.cwd()):
            raise ValueError(
                "Config tasks_dir invalid, must be inside the current working directory"
            )

        _assert_tasks_dir_path_is_valid(Path(config["tasks_dir"]))
        return Config(tasks_dir=Path(config["tasks_dir"]))
    return None


def get_config_path() -> Path:
    return Path.cwd() / CONFIG_FILENAME


def write_config(config: Config) -> None:
    _assert_tasks_dir_path_is_valid(config.tasks_dir)
    with open(CONFIG_FILENAME, "w") as f:
        f.write(f'tasks_dir = "{config.tasks_dir}"\n')


def assert_initialised() -> None:
    if not Path(CONFIG_FILENAME).exists():
        raise RuntimeError("tasks not initialised, run: tasks --help")
