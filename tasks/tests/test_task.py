import dataclasses
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent

import pytest

from tasks import actions
from tasks.actions._read import HeaderAttrs, _parse_header
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

    def test_create_task_removes_newlines_from_name(self):
        task = actions.create_task(name="foo\nand\n\nbar\n\n")
        assert task.filename == "foo_and_bar_.md"
        assert task.name == "foo and bar"


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


class TestReadTask:
    def test_read_task_matches_persisted_task(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello\nTask!")
        actions.persist_task(task)
        task_after_read = actions.read_task(init_result.tasks_dir / task.filename)
        assert task_after_read == task

    def test_read_task_throws_if_filepath_does_not_exist(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init_result = init(tasks_dir=Path("my/tasks"))
        not_exists_path = init_result.tasks_dir / "not_a_task.md"
        with pytest.raises(FileNotFoundError, match=f"Task not found at: {not_exists_path}"):
            actions.read_task(not_exists_path)

    def test_body_can_contain_header_split(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        init_result = init(tasks_dir=Path("my/tasks"))
        task = actions.create_task(name="Hello Task")

        body_text = dedent("""\
            # Hello Task!
            
            ---

            Some stuff to do...
        """)
        task_with_header_split_in_body = dataclasses.replace(task, body=body_text)
        actions.persist_task(task_with_header_split_in_body)

        result = actions.read_task(init_result.tasks_dir / task_with_header_split_in_body.filename)
        assert result.body == body_text

    def test_parse_header(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            status: todo
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
            
            Some stuff to do...
        """)
        result = _parse_header(file_text)
        expected = HeaderAttrs(
            name="Hello Task!",
            status=TaskStatus.TODO,
            created_by="the creator",
            created_at=datetime(2030, 12, 12, 15, 0, 1),
        )
        assert result == expected

    def test_parse_header_can_parse_values_with_separator_in_them(self):
        file_text = dedent("""\
            ---
            name: Hello Ta: sk!
            status: todo
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!

            Some stuff to do...
        """)
        result = _parse_header(file_text)
        assert result.name == "Hello Ta: sk!"

    def test_parse_header_is_relatively_liberal(self):
        file_text = dedent("""\
        
        
            -----
            
            
            name:   Hello Task!
            
            status:     todo
            created_by:     the creator
            
            created_at:   2030-12-12 15:00:01
            
            --------
            # Hello Task!

            Some stuff to do...
        """)
        result = _parse_header(file_text)
        expected = HeaderAttrs(
            name="Hello Task!",
            status=TaskStatus.TODO,
            created_by="the creator",
            created_at=datetime(2030, 12, 12, 15, 0, 1),
        )
        assert result == expected

    def test_parse_header_raises_if_first_line_not_dashes(self):
        file_text = dedent("""\
            not dashes
            ---
            name: Hello Task!
            status: todo
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match="Task file must start with header on first line: ---"):
            _parse_header(file_text)

    def test_parse_header_raises_if_datetime_not_parseable(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            status: todo
            created_by: the creator
            created_at: NOT 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match="Invalid isoformat string: 'NOT 2030-12-12 15:00:01'"):
            _parse_header(file_text)

    def test_parse_header_raises_if_status_not_TaskStatus(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            status: not-todo
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match="'not-todo' is not a valid TaskStatus"):
            _parse_header(file_text)

    def test_parse_header_raises_if_header_missing_name(self):
        file_text = dedent("""\
            ---

            status: not-todo
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match='Task header invalid: missing "name"'):
            _parse_header(file_text)

    def test_parse_header_raises_if_header_missing_status(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            created_by: the creator
            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match='Task header invalid: missing "status"'):
            _parse_header(file_text)

    def test_parse_header_raises_if_header_missing_created_by(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            status: not-todo

            created_at: 2030-12-12 15:00:01
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match='Task header invalid: missing "created_by"'):
            _parse_header(file_text)

    def test_parse_header_raises_if_header_missing_created_at(self):
        file_text = dedent("""\
            ---
            name: Hello Task!
            status: not-todo
            created_by: the creator
            ---
            # Hello Task!
        """)
        with pytest.raises(ValueError, match='Task header invalid: missing "created_at"'):
            _parse_header(file_text)


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
