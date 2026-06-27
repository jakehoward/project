from datetime import datetime
from pathlib import Path

from tasks import actions
from tasks.actions import persist_task
from tasks.commands import init
from tasks.task import MAX_ATTR_VALUE_LENGTH, TaskStatus


class TestCreateTask:
    def test_create_task_defaults(self):
        now = datetime.now()

        task = actions.create_task(name="foo", now=lambda: now, get_who=lambda: "It was me!")

        assert task.filename == "foo.md"
        assert task.name == "foo"
        assert "foo" in task.body

        assert task.metadata.status == TaskStatus.TODO
        assert task.metadata.created_at == now
        assert task.metadata.created_by == "It was me!"

    def test_create_task_normalises_filename(self):
        task = actions.create_task(name="foo and bar")
        assert task.filename == "foo_and_bar.md"
        assert task.name == "foo and bar"

    def test_get_who_content_is_sanitised(self):
        task = actions.create_task(
            name="foo", get_who=lambda: "This \n\n is not \n\n ok" + 100 * "x"
        )
        prefix = "This  is not  ok"
        assert task.metadata.created_by == prefix + (MAX_ATTR_VALUE_LENGTH - len(prefix)) * "x"


class TestPersistTask:
    def test_persist_task_writes_a_file(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello Task")
        persist_task(task)
        assert (init_result.tasks_dir / task.filename).exists()

    def test_persist_task_writes_a_task_header(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        init_result = init(tasks_dir=Path("my/tasks"))
        the_now = datetime(2030, 12, 12, 15, 0, 1)
        task = actions.create_task(
            name="Hello Task", get_who=lambda: "the creator", now=lambda: the_now
        )
        persist_task(task)
        expected_header = [
            "---",
            "name: Hello Task",
            "status: todo",
            "created_by: the creator",
            "created_at: 2030-12-12 15:00:01",
            "---",
        ]
        file_text = (init_result.tasks_dir / task.filename).read_text()
        actual_header = "\n".join(file_text.splitlines()[0 : len(expected_header)])
        assert actual_header == "\n".join(expected_header)

    def test_persist_task_writes_a_body(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello Task")

        persist_task(task)

        file_lines = (init_result.tasks_dir / task.filename).read_text().splitlines()
        second_dashes_idx = file_lines[1:].index("---") + 1
        actual_body = "\n".join(file_lines[second_dashes_idx + 1 :])
        assert actual_body == task.body.rstrip("\n")
