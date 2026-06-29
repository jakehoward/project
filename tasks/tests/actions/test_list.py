from datetime import datetime, timedelta
from pathlib import Path

from tasks import actions
from tasks.commands import init


class TestListTasks:
    def test_list_tasks_returns_empty_list_when_no_tasks_exist(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init(tasks_dir=Path("tasks"))
        tasks = actions.list_tasks()
        assert tasks == []

    def test_list_tasks_returns_a_single_task(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello Task")
        actions.persist_task(task)

        tasks = actions.list_tasks()
        assert tasks == [task]

    def test_list_tasks_returns_multiple_tasks_ordered_by_created_at_desc(
        self, tmp_path: Path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        init(tasks_dir=Path("my/tasks"))
        first_now = datetime.now()
        task = actions.create_task(name="Hello Task", now=lambda: first_now)
        actions.persist_task(task)

        second_now = first_now + timedelta(seconds=1)
        nh_task = actions.create_task(name="Not Hello Task", now=lambda: second_now)
        actions.persist_task(nh_task)

        tasks = actions.list_tasks()
        assert tasks == [nh_task, task]
