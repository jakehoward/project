import pytest

from tasks.utils import normalise_name


class TestNormaliseName:
    @pytest.mark.parametrize(
        "name, expected",
        [
            ("hello", "hello"),
            ("Hello World", "Hello_World"),
            ("hello\tworld", "hello_world"),
            ("hello\n world", "hello_world"),
            ("hello_world", "hello_world"),
            ("hello-world", "hello-world"),
            (
                "A very important task && !@#$%^&*() other things",
                "A_very_important_task__other_things",
            ),
        ],
    )
    def test_normalise_name(self, name, expected):
        assert normalise_name(name) == expected

    def test_normalise_name_raises_if_only_underscores_left(self):
        with pytest.raises(
            ValueError, match="name cannot be normalised - use a-zA-Z0-9 in the task name"
        ):
            normalise_name("$%^&")

    def test_normalise_name_truncates_overly_long_names(self):
        max_len = 50
        assert normalise_name((max_len + 1) * "x") == max_len * "x"
