import tomllib
from pathlib import Path

import pytest

from tasks.commands._init import init
from tasks.config import CONFIG_FILENAME, Config, assert_initialised, read_config, write_config


def test_write_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert not Path(CONFIG_FILENAME).exists()
    write_config(Config(tasks_dir=Path("./foo/bar/tasks")))
    assert Path(CONFIG_FILENAME).exists()

    with open(CONFIG_FILENAME, "rb") as f:
        config = tomllib.load(f)
    assert config == {"tasks_dir": "foo/bar/tasks"}


def test_read_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    write_config(Config(tasks_dir=Path("./foo/baz/tasks")))
    assert read_config() == Config(tasks_dir=Path("foo/baz/tasks"))


def test_read_config_throws_if_path_not_relative_to_cwd(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    write_config(Config(tasks_dir=Path("./foo/baz/tasks")))
    with open(Path.cwd() / CONFIG_FILENAME, "w") as f:
        f.write('tasks_dir = "../outside"')

    with pytest.raises(
        ValueError,
        match="Config tasks_dir invalid, must be inside the current working directory",
    ):
        read_config()


def test_read_config_throws_if_tasks_dir_not_present(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    write_config(Config(tasks_dir=Path("./foo/baz/tasks")))
    with open(Path.cwd() / CONFIG_FILENAME, "w") as f:
        f.write('nope = "foo"')

    with pytest.raises(
        ValueError,
        match=f"Invalid Config: 'tasks_dir' is missing in {CONFIG_FILENAME}",
    ):
        read_config()


def test_write_throws_if_tasks_dir_contains_double_quote(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    invalid_path = 'foo/baz/t"asks'
    with pytest.raises(
        ValueError,
        match=f"Invalid Config: 'tasks_dir' path cannot contain double quote: {invalid_path}",
    ):
        write_config(Config(tasks_dir=Path(invalid_path)))


def test_read_throws_if_tasks_dir_contains_double_quote(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    write_config(Config(tasks_dir=Path("./foo/baz/tasks")))
    invalid_path = 'foo/baz/t\\"asks'
    with open(Path.cwd() / CONFIG_FILENAME, "w") as f:
        f.write(f'"tasks_dir" = "{invalid_path}"')

    with pytest.raises(
        ValueError, match="Invalid Config: 'tasks_dir' path cannot contain double quote"
    ):
        read_config()


def test_assert_initialised_raises_if_not_init(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError, match="tasks not initialised, run: tasks --help"):
        assert_initialised()


def test_assert_initialised_not_raises_if_init(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("tasks"))
    assert_initialised()  ## does not raise
