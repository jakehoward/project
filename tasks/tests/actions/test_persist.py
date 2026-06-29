from datetime import datetime
from pathlib import Path

from tasks import actions
from tasks.commands import init


class TestPersistTask:
    def test_persist_task_writes_a_file(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello Task")
        actions.persist_task(task)
        assert (init_result.tasks_dir / task.filename).exists()

    def test_persist_task_writes_a_task_header(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        init_result = init(tasks_dir=Path("my/tasks"))
        the_now = datetime(2030, 12, 12, 15, 0, 1)
        task = actions.create_task(
            name="Hello Task", get_who=lambda: "the creator", now=lambda: the_now
        )
        actions.persist_task(task)
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

        actions.persist_task(task)

        file_lines = (init_result.tasks_dir / task.filename).read_text().splitlines()
        second_dashes_idx = file_lines[1:].index("---") + 1
        actual_body = "\n".join(file_lines[second_dashes_idx + 1 :])
        assert actual_body == task.body.rstrip("\n")

    def test_persist_task_writes_a_single_line_name_to_header(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello\nTask\nwith\n\nnewlines")
        actions.persist_task(task)
        expected_header = [
            "---",
            "name: Hello Task with newlines",
        ]
        file_text = (init_result.tasks_dir / task.filename).read_text()
        actual_header = "\n".join(file_text.splitlines()[0 : len(expected_header)])
        assert actual_header == "\n".join(expected_header)
