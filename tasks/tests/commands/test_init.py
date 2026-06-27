from pathlib import Path

import pytest

from tasks.commands.init import init
from tasks.config import CONFIG_FILENAME, Config, read_config


def test_init_clean_project(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    init(tasks_dir=(tmp_path / "tasks"))
    assert (tmp_path / "tasks").is_dir()

    assert (tmp_path / CONFIG_FILENAME).exists()
    assert read_config() == Config(tasks_dir=Path("tasks"))


def test_init_handles_relative_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    init(tasks_dir=Path("./my-tasks"))
    assert read_config() == Config(tasks_dir=Path("my-tasks"))


def test_init_handles_nested_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    init(tasks_dir=Path("./my-tasks/foo/tasks"))
    assert (tmp_path / "my-tasks/foo/tasks").is_dir()
    assert read_config() == Config(tasks_dir=Path("my-tasks/foo/tasks"))


def test_init_raises_if_task_dir_already_exists_writing_no_config(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir(parents=True)
    with pytest.raises(FileExistsError, match="Init Error: tasks dir already exists"):
        init(tasks_dir=tasks_dir)
    assert not (Path.cwd() / CONFIG_FILENAME).exists()


def test_init_raises_if_task_dir_not_is_relative_to_cwd(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="Tasks dir must be inside the current working directory"):
        init(tasks_dir=(tmp_path / "../tasks"))


def test_init_raises_if_task_dir_not_is_relative_to_cwd_2(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="Tasks dir must be inside the current working directory"):
        init(tasks_dir=Path("../tasks"))


def test_init_raises_if_config_already_exists(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=(tmp_path / "tasks"))

    with pytest.raises(FileExistsError, match='Config already exists. Tasks dir set to: "tasks"'):
        init(tasks_dir=(tmp_path / "some_other_dir"))


def test_init_writes_a_gitkeep_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("./my-tasks/foo/tasks"))

    assert (tmp_path / "my-tasks/foo/tasks/.gitkeep").is_file()


def test_init_returns_info_about_where_it_put_things(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rel_path = Path("./my-tasks/foo/tasks")
    res = init(tasks_dir=rel_path)
    assert res.tasks_dir == rel_path.resolve()
    # slight DRY violation, but better a false negative (test fails)
    assert res.config_file == tmp_path / CONFIG_FILENAME
