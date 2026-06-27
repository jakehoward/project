from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIG_FILENAME = ".tasks.json"


@dataclass(frozen=True)
class Config:
    tasks_dir: Path


def read_config() -> Config | None:
    if Path(CONFIG_FILENAME).exists():
        with open(CONFIG_FILENAME) as f:
            config = json.load(f)

        if "tasks_dir" not in config:
            raise ValueError(f"Invalid Config: 'tasks_dir' is missing in {CONFIG_FILENAME}")
        if not Path(config["tasks_dir"]).resolve().is_relative_to(Path.cwd()):
            raise ValueError(
                "Config tasks_dir invalid, must be inside the current working directory"
            )

        return Config(tasks_dir=Path(config["tasks_dir"]))
    return None


def get_config_path() -> Path:
    return Path.cwd() / CONFIG_FILENAME


def write_config(config: Config) -> None:
    with open(CONFIG_FILENAME, "w") as f:
        json.dump(asdict(config), f, default=str)


def assert_initialised() -> None:
    if not Path(CONFIG_FILENAME).exists():
        raise RuntimeError("tasks not initialised, run: tasks --help")
