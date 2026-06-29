from datetime import datetime

from tasks import actions
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
