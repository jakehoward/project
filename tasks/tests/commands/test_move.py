from pathlib import Path

import pytest

from tasks import actions
from tasks.commands import init, move_task
from tasks.task import TaskStatus


def test_move_task_raises_if_not_initialised(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError):
        move_task(Path("my/tasks/foo.md"), TaskStatus.DOING)


def test_move_task_raises_if_no_task_at_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    with pytest.raises(FileNotFoundError, match="Task not found at: foo/here.md"):
        move_task(path_to_task=Path("foo/here.md"), new_status=TaskStatus.DOING)


def test_move_task_raises_if_task_already_has_status_of_new_status(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    task = actions.create_task(name="some-task")
    actions.persist_task(task)

    existing_status = TaskStatus.TODO
    assert task.metadata.status == existing_status

    with pytest.raises(
        ValueError, match=f"Error: task {task.name} already has status {existing_status}"
    ):
        move_task(path_to_task=Path("foo/some-task.md"), new_status=existing_status)


def test_move_task_changes_status_of_task(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    task = actions.create_task(name="some-task")
    actions.persist_task(task)

    assert task.metadata.status == TaskStatus.TODO
    updated_task = move_task(path_to_task=Path("foo/some-task.md"), new_status=TaskStatus.DOING)
    disk_task = actions.read_task(tmp_path / "foo" / task.filename)
    assert disk_task == updated_task
    assert disk_task.metadata.status == TaskStatus.DOING
