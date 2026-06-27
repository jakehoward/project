from pathlib import Path

import pytest

from tasks.commands import add_task, init


def test_add_task_raises_if_not_initialised(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError):
        add_task("foo")


def test_add_task_raises_if_no_name(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    with pytest.raises(ValueError, match="Add task must provide a name"):
        add_task("")
    with pytest.raises(ValueError, match="Add task must provide a name"):
        add_task(None)  # type: ignore[arg-type]


def test_add_task_raises_if_normalised_name_is_duplicate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    add_task("my_&&_name")
    with pytest.raises(ValueError, match="Task with filename my__name.md already exists"):
        add_task("my_**_name")


def test_add_task_creates_file_with_normalised_name(tmp_path: Path, monkeypatch) -> None:
    # Some DRY violation here, but ok with false negative (test fails for no good reason) for now
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    add_task("A very important task && !@#$%^&*() other things")
    expected_filepath = tmp_path / "foo" / "A_very_important_task__other_things.md"
    assert expected_filepath.exists()
    assert expected_filepath.is_file()
    assert "# A very important task && !@#$%^&*() other things" in expected_filepath.read_text()
