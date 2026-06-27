from datetime import datetime

import pytest

from tasks.task import (
    MAX_ATTR_VALUE_LENGTH,
    MAX_FILENAME_LEN,
    TaskStatus,
    _normalise_name,
    create_task,
    default_template,
)


def test_create_task_defaults():
    now = datetime.now()

    task = create_task(name="foo", now=lambda: now, get_who=lambda: "It was me!")

    assert task.filename == "foo.md"
    assert task.name == "foo"
    assert task.body == default_template(name="foo")

    assert task.metadata.status == TaskStatus.TODO
    assert task.metadata.created_at == now
    assert task.metadata.created_by == "It was me!"


def test_create_task_normalises_filename():
    task = create_task(name="foo and bar")
    assert task.filename == "foo_and_bar.md"
    assert task.name == "foo and bar"


def test_get_who_content_is_sanitised():
    task = create_task(name="foo", get_who=lambda: "This \n\n is not ok" + 100 * "x")
    prefix = "This  is not ok"
    assert task.metadata.created_by == prefix + (MAX_ATTR_VALUE_LENGTH - len(prefix)) * "x"


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


def test_normalise_name_truncates_overly_long_names():
    assert _normalise_name((MAX_FILENAME_LEN + 1) * "x") == MAX_FILENAME_LEN * "x"
