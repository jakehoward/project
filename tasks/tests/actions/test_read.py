import dataclasses
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import pytest

from tasks import actions
from tasks.actions._read import HeaderAttrs, _parse_header
from tasks.commands import init
from tasks.task import TaskStatus


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
