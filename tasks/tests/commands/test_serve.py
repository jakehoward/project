from pathlib import Path

from tasks import actions
from tasks.commands import init
from tasks.kanban._http_helpers import Method
from tasks.kanban._kanban import handle


def test_get_root_returns_200_with_link_to_tasks() -> None:
    status, headers, body = handle(Method.GET, "/")
    assert status == 200
    assert headers == {"content-type": "text/html; charset=utf-8"}
    assert '<a href="/tasks">Tasks</a>' in str(body, encoding="utf-8")


def test_empty_tasks() -> None:
    status, headers, body = handle(Method.GET, "/tasks")
    assert status == 200
    assert headers == {"content-type": "text/html; charset=utf-8"}
    assert "<h1>Tasks</h1>" in str(body, encoding="utf-8")


def test_single_task(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    task = actions.create_task(name="some-task-123abc")
    actions.persist_task(task)

    status, headers, body = handle(Method.GET, "/tasks")

    assert status == 200
    assert headers == {"content-type": "text/html; charset=utf-8"}
    assert "some-task-123abc" in str(body, encoding="utf-8")


def test_multiple_tasks(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init(tasks_dir=Path("foo"))
    task = actions.create_task(name="some-task-123abc")
    actions.persist_task(task)
    task = actions.create_task(name="another-task-456def")
    actions.persist_task(task)

    status, headers, body = handle(Method.GET, "/tasks")

    assert status == 200
    assert headers == {"content-type": "text/html; charset=utf-8"}
    assert "some-task-123abc" in str(body, encoding="utf-8")
    assert "another-task-456def" in str(body, encoding="utf-8")


def test_404() -> None:
    status, headers, body = handle(Method.GET, "/not-a-thing")
    assert status == 404
    assert headers == {"content-type": "text/html; charset=utf-8"}
    assert "Not found" in str(body, encoding="utf-8")
