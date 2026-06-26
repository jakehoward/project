from pathlib import Path

import pytest

from tasks.commands.add import _normalise_name, add
from tasks.commands.init import init


def test_raises_if_not_initialised(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError):
        add("foo")


def test_raises_if_no_name(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    with pytest.raises(ValueError, match="Add task must provide a name"):
        add("")
    with pytest.raises(ValueError, match="Add task must provide a name"):
        add(None)  # type: ignore[arg-type]


def test_raises_if_normalised_name_is_duplicate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    add("my_&&_name")
    with pytest.raises(ValueError, match="Task with name my__name already exists"):
        add("my_**_name")


def test_creates_file_with_normalised_name(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    add("A very important task && !@#$%^&*() other things")
    expected_filepath = tmp_path / "foo" / "A_very_important_task__other_things.md"
    assert expected_filepath.exists()
    assert expected_filepath.is_file()
    assert "# A very important task && !@#$%^&*() other things" in expected_filepath.read_text()


@pytest.mark.parametrize(
    "name, expected",
    [
        ("hello", "hello"),
        ("Hello World", "Hello_World"),
        ("hello\tworld", "hello_world"),
        ("hello\n world", "hello_world"),
        ("hello_world", "hello_world"),
        ("hello-world", "hello-world"),
        ("A very important task && !@#$%^&*() other things", "A_very_important_task__other_things"),
    ],
)
def test_normalise_name(name, expected):
    assert _normalise_name(name) == expected


def test_normalise_name_raises_if_only_underscores_left():
    with pytest.raises(
        ValueError, match="name cannot be normalised - use a-zA-Z0-9 in the task name"
    ):
        _normalise_name("$%^&")
